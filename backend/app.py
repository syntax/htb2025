from flask import Flask, jsonify, request, abort
import ccxt
import pandas as pd
import numpy as np
import requests
from sentimentanaly import compute_sentiment_scores
import database
import risk
from models import Portfolio, Crypto, PortfolioObject
import ethical
from flask_cors import CORS
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the HTB2025 API",
        "status": "success"
    }), 200

@app.route('/store_crypto_data', methods=['GET'])
def store_crypto_data():
    db = database.Database()

    # Retrieve real-time symbol data from CSV
    symbol_data = pd.read_csv("backend/ethical_data/environmental_ratings.csv")
    symbol_data.columns = symbol_data.columns.str.lower()
    
    symbol_data.loc[symbol_data["ticker"] == "xrp", "volatility"] = 0.05


    # Ensure risk and ethics values recalculated before updating table
    risk_scores_df = risk.calculate_risk_score(symbol_data)
    ethics_scores_df = ethical.process_crypto_data(symbol_data)
    

    for _, entry in symbol_data.iterrows():
        risk_score = risk_scores_df.loc[risk_scores_df['ticker'] == entry.get("ticker"), 'risk_score'].values
        risk_score = risk_score[0] if len(risk_score) > 0 else 0.0
        ethics_score = ethics_scores_df.loc[ethics_scores_df['ticker'] == entry.get("ticker"), 'ethical impact'].values
        ethics_score = ethics_score[0] if len(ethics_score) > 0 else 0.0
        
        
        db.update_crypto(   
            ticker=entry.get("ticker"),
            name=entry.get("name"),
            consensus=entry.get("consensus"),
            market_cap=entry.get("market_cap"),
            power_consumption=entry.get("power_consumption"),
            annual_energy_consumption=entry.get("annual_energy_consumption"),
            carbon_emissions=entry.get("carbon_emissions"),
            average_liquidity=entry.get("average_liquidity", "Unknown"),
            volatility=entry.get("volatility"),
            normalized_energy=entry.get("normalized_energy"),
            normalized_carbon=entry.get("normalized_carbon"),
            raw_environmental_score=entry.get("raw_environmental_score"),
            environmental_score=entry.get("environmental_score"),
            risk_score=risk_score,
            ethics_score = ethics_score
        )


    #Update and recalculate all risk and ethics values for portfolios
    # Retrieve and update all portfolios
    portfolios = db.get_all_portfolios()
    for portfolio in portfolios:
        portfolio.update_total_risk(db.session)
        portfolio.update_total_ethics(db.session)
        db.update_portfolio(portfolio)
        

    db.close_connection()
    
    return jsonify({"message": "Success"}), 200


@app.route('/api/sentiment', methods=['GET'])
def get_ethics_sentiment():
    """
    Get sentiment for a given cryptocurrency ticker.
    Query parameters:
      - ticker: cryptocurrency ticker symbol
    """
    ticker = request.args.get('ticker', 'SC')

    # mock data at this csv cos tweety rate limits us so quick
    csv_file = "utils/crypto_tweets.csv"
    ethics_score, risk_score = compute_sentiment_scores(csv_file, ticker)
    return jsonify({
        "ticker": ticker,
        "ethics_score": ethics_score,
        "risk_score": risk_score
    }), 200

@app.route('/get_portfolio_value_by_coin/<int:user_id>', methods=['GET'])    
def get_portfolio_value_by_coin(user_id):
    db = database.Database()
    portfolio = db.get_portfolio(user_id)
    db.close_connection()
    
    new_map = {}
    
    for coin_id, amount in portfolio.holdings.items():
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        print(response)
        
        if response.status_code == 200:
            data = response.json()
            price = data.get(coin_id, {}).get("usd", 0)
            new_map[coin_id] = price * amount  # Calculate total value per coin
        else:
            new_map[coin_id] = None  # Handle failed requests gracefully
    
    
    return jsonify(new_map), 200
    
    
@app.route('/api/get_knn_coords/<int:user_id>', methods=['GET'])    
def get_knn_coords(user_id):
    db = database.Database()
    portfolio = db.get_portfolio(user_id)
    db.close_connection()
    
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404
    
    holdings = portfolio.holdings
    coins = holdings.keys()
    crypto_map = {}

    # for each coin, query the database for the crypto object and store it in a map
    for coin in coins:
        crypto = db.get_crypto(coin)
        if crypto:
            crypto_map[coin] = [crypto.risk_score, crypto.ethics_score]
        else:
            crypto_map[coin] = None
    
    crypto_map["user_score"] = [portfolio.user_risk_score, portfolio.user_ethics_score]

    return jsonify(crypto_map), 200
    
    
    # go through the cryptos in cryptos and get the risk and ethics scores
    crypto_data = pd.DataFrame([{
        'ticker': c.ticker,
        'risk_score': c.risk_score,
        'ethics_score': c.ethics_score
    } for c in cryptos])
@app.route('/api/submit_user_phone_number', methods=['POST'])
def submit_user_phone_number():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        phone_number = data.get('phone_number')
        
        if not user_id or not phone_number:
            return jsonify({"error": "Missing user_id or phone_number"}), 400
        
        db = database.Database()
        portfolio = db.get_portfolio(user_id)
        
        # Create new portfolio if it doesn't exist
        if not portfolio:
            portfolio = PortfolioObject(user_id)
        
        portfolio.phone_number = phone_number
        print(phone_number)
        
        db.add_portfolio(portfolio)
        db.close_connection()
        
        return jsonify({"message": "Phone number updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/submit_user_scores', methods=['POST'])
def submit_user_scores():
    try:
        data = request.get_json()
        
        if not data or "risk_score" not in data or "ethics_score" not in data:
            return jsonify({"error": "Missing risk_score or ethics_score"}), 400
        
        user_id = "123"
        risk_score = data["risk_score"]
        ethics_score = data["ethics_score"]

        print(f"Received Scores - Risk: {risk_score}, Ethics: {ethics_score}")


        db = database.Database()
        portfolio = db.get_portfolio(user_id)

        if not portfolio:
            portfolio = PortfolioObject(user_id)
        
        # Update user scores
        portfolio.user_risk_score = risk_score
        portfolio.user_ethics_score = ethics_score

        db.add_portfolio(portfolio)
        db.close_connection()


        return jsonify({"message": "Scores received successfully!"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/generate_portfolio/<int:user_id>', methods=['GET'])
def generate_portfolio(user_id):
    # try:
    db = database.Database()
    portfolio = db.get_portfolio(user_id)
   
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404
    
    if portfolio.user_risk_score == 0 or portfolio.user_ethics_score == 0:
        return jsonify({"error": "User scores not submitted"}), 400
    
    cryptos = db.session.query(Crypto).all()
    
    if not cryptos:
        return jsonify({"error": "No crypto data available"}), 404
    
    crypto_data = pd.DataFrame([{
        'ticker': c.ticker,
        'risk_score': c.risk_score,
        'ethics_score': c.ethics_score
    } for c in cryptos])

    if len(crypto_data) < 5:
        return jsonify({"error": "Not enough cryptocurrencies in database"}), 400

    n_neighbors = min(10, len(crypto_data))  # Adjust based on available data
    knn = NearestNeighbors(n_neighbors=4, algorithm='ball_tree')
    knn.fit(crypto_data[['risk_score', 'ethics_score']].values)
    
    _, indices = knn.kneighbors([[portfolio.user_risk_score, portfolio.user_ethics_score]])
    
    top_n = min(5, len(indices[0]))
    selected_indices = indices[0][:top_n]
    selected_cryptos = crypto_data.iloc[selected_indices]
    
    allocation = {
        row['ticker']: 1.0/top_n 
        for _, row in selected_cryptos.iterrows()
    }
    
    portfolio.holdings = allocation
    
    portfolio.update_total_risk(db.session)
    portfolio.update_total_ethics(db.session)
    
    db.add_portfolio(portfolio)
    db.close_connection()

    return jsonify({
        "message": "Portfolio generated using KNN",
        "holdings": allocation,
        "total_risk": portfolio.total_risk,
        "total_ethics": portfolio.total_ethics,
        "selected_cryptos": selected_cryptos.to_dict(orient='records')
    }), 200

    # except Exception as e:
    #     print("Error:", str(e))
    #     print(e.with_traceback())
    #     return jsonify({"error": "Internal server error"}), 500
    

@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    exchange_id = request.args.get('exchange')
    symbol = request.args.get('symbol')
    result = {}

    if exchange_id:
        try:
            exchange_class = getattr(ccxt, exchange_id)
        except AttributeError:
            abort(400, description=f"Exchange {exchange_id} is not supported by CCXT.")
        exchange = exchange_class()
        exchange.load_markets()

        if symbol:
            if symbol in exchange.symbols:
                try:
                    symbol = exchange.fetch_symbol(symbol)
                    result[exchange_id] = symbol
                except Exception as e:
                    result[exchange_id] = {"error": str(e)}
            else:
                result[exchange_id] = {"error": f"{symbol} is not available on {exchange_id}"}
        else:
            try:
                symbols = exchange.fetch_symbols()
                result[exchange_id] = symbols
            except Exception as e:
                result[exchange_id] = {"error": str(e)}
    else:
        default_exchanges = ['binance', 'kraken']
        for ex in default_exchanges:
            try:
                exchange_class = getattr(ccxt, ex)
            except AttributeError:
                result[ex] = {"error": "Exchange not supported"}
                continue
            exchange = exchange_class()
            exchange.load_markets()
            if symbol:
                if symbol in exchange.symbols:
                    try:
                        symbol = exchange.fetch_symbol(symbol)
                        result[ex] = symbol
                    except Exception as e:
                        result[ex] = {"error": str(e)}
                else:
                    result[ex] = {"error": f"{symbol} is not available on {ex}"}
            else:
                try:
                    symbols = exchange.fetch_symbols()
                    result[ex] = symbols
                except Exception as e:
                    result[ex] = {"error": str(e)}
    return jsonify(result), 200

@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """
    calc volatility using historical OHLCV data.
    Query parameters:
      - exchange (default: binance)
      - symbol (default: BTC/USDT)
      - timeframe (default: 1h)
      - limit: number of candles to fetch for base calculation (default: 100)
    we also, calculates volatility over roughly 1 month and 6 months.
    """
    exchange_id = request.args.get('exchange', 'binance')
    symbol = request.args.get('symbol', 'BTC/USDT')
    timeframe = request.args.get('timeframe', '1h')
    limit = int(request.args.get('limit', 100))
    
    try:
        exchange_class = getattr(ccxt, exchange_id)
    except AttributeError:
        abort(400, description=f"Exchange {exchange_id} is not supported by CCXT.")
    exchange = exchange_class()
    exchange.load_markets()
    
    if symbol not in exchange.symbols:
        return jsonify({"error": f"{symbol} is not available on {exchange_id}"}), 400
    
    # base volatility calculation using provided limit
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['log_return'] = np.log(df['close'] / df['close'].shift(1))
    volatility = df['log_return'].std()
    
    if timeframe.endswith('h'):
        annual_factor = (24 * 365) ** 0.5
    elif timeframe.endswith('d'):
        annual_factor = (365) ** 0.5
    else:
        annual_factor = 1
    annualized_volatility = volatility * annual_factor

    # det limits for monthly and 6-month calculations based on timeframe
    if timeframe.endswith('d'):
        monthly_limit = 30      # approximately 1 month
        six_month_limit = 180   # approximately 6 months
    elif timeframe.endswith('h'):
        monthly_limit = 24 * 30      # hourly candles for 30 days
        six_month_limit = 24 * 180   # hourly candles for 180 days
    else:
        monthly_limit = limit
        six_month_limit = limit
    
    # monht volatility calculation
    try:
        ohlcv_month = exchange.fetch_ohlcv(symbol, timeframe, limit=monthly_limit)
        df_month = pd.DataFrame(ohlcv_month, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_month['timestamp'] = pd.to_datetime(df_month['timestamp'], unit='ms')
        df_month['log_return'] = np.log(df_month['close'] / df_month['close'].shift(1))
        monthly_volatility = df_month['log_return'].std()
    except Exception as e:
        monthly_volatility = None

    #6month volatility calculation
    try:
        ohlcv_6month = exchange.fetch_ohlcv(symbol, timeframe, limit=six_month_limit)
        df_6month = pd.DataFrame(ohlcv_6month, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df_6month['timestamp'] = pd.to_datetime(df_6month['timestamp'], unit='ms')
        df_6month['log_return'] = np.log(df_6month['close'] / df_6month['close'].shift(1))
        six_month_volatility = df_6month['log_return'].std()
    except Exception as e:
        six_month_volatility = None

    return jsonify({
        "exchange": exchange_id,
        "symbol": symbol,
        "timeframe": timeframe,
        "base_data_points": len(df),
        "volatility": volatility,
        "annualized_volatility": annualized_volatility,
        "monthly_data_points": len(df_month) if 'df_month' in locals() else 0,
        "monthly_volatility": monthly_volatility,
        "six_month_data_points": len(df_6month) if 'df_6month' in locals() else 0,
        "six_month_volatility": six_month_volatility
    }), 200


@app.route('/api/liquidity', methods=['GET'])
def get_liquidity():
    """
    Estimate liquidity using trading volume as a proxy.
    Query parameters:
      - exchange (default: binance)
      - symbol (default: BTC/USDT)
      - timeframe (default: 1h)
      - limit: number of candles to fetch (default: 100)
    """
    # exchange_id = request.args.get('exchange', 'binance')
    # symbol = request.args.get('symbol', 'BTC/USDT')
    # timeframe = request.args.get('timeframe', '1h')
    # limit = int(request.args.get('limit', 100))
    exchange_id = request.args.get('exchange', 'binance')
    symbol = request.args.get('symbol', 'BTC/USDT')
    timeframe = request.args.get('timeframe', '1h')
    limit = int(request.args.get('limit', 100))
    
    try:
        exchange_class = getattr(ccxt, exchange_id)
    except AttributeError:
        abort(400, description=f"Exchange {exchange_id} is not supported by CCXT.")
    exchange = exchange_class()
    exchange.load_markets()
    
    if symbol not in exchange.symbols:
        return jsonify({"error": f"{symbol} is not available on {exchange_id}"}), 400
    
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # this is using average trading volume as a proxy for liquidity.
    avg_volume = df['volume'].mean()
    
    return jsonify({
        "exchange": exchange_id,
        "symbol": symbol,
        "timeframe": timeframe,
        "average_volume": avg_volume,
        "data_points": len(df)
    }), 200

# API Route to Get a Specific Portfolio by User ID
@app.route('/portfolio/<int:user_id>', methods=['GET'])
def get_portfolio(user_id):
    db = database.Database()
    portfolio = db.get_portfolio(user_id)
    print("ETHICS:", portfolio.total_ethics)
    db.close_connection()
    if portfolio:
        return jsonify(portfolio.__dict__)
    else:
        return jsonify({"error": "User portfolio not found"}), 404


@app.route('/api/all_symbol_info', methods=['GET'])
def get_all_symbol_info():
    """
    Build a dataframe of symbol data for multiple symbols along with liquidity and volatility metrics.
    Query parameters:
      - exchange (default: binance)
      - timeframe for OHLCV data (default: 1h)
      - limit: number of OHLCV candles to fetch (default: 100)
      - max: maximum number of symbols to process (default: 10)
    
    NOTE: Not sure if this is gonna fuck us a bit re rate limits. watch out fellas.
    """
    exchange_id = request.args.get('exchange', 'binance')
    timeframe = request.args.get('timeframe', '1h')
    ohlcv_limit = int(request.args.get('limit', 100))
    max_symbols = int(request.args.get('max', 10))
    
    try:
        exchange_class = getattr(ccxt, exchange_id)
    except AttributeError:
        abort(400, description=f"Exchange {exchange_id} is not supported by CCXT.")
    exchange = exchange_class()
    exchange.load_markets()
    markets = exchange.fetch_markets()
    symbols = [market['symbol'] for market in markets]
    


    # Process a limited number of symbols to avoid overload
    symbols = symbols[:max_symbols]
    results = []
    
    for symbol in symbols:
        if symbol not in exchange.symbols:
            continue
        info = {"symbol": symbol}
        
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=ohlcv_limit)
        except Exception as e:
            info["error"] = f"Failed to fetch OHLCV: {str(e)}"
            results.append(info)
            continue
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # litquidity: average volume
        avg_volume = df['volume'].mean()
        info["average_volume"] = avg_volume
        
        # vol: using log returns from OHLCV
        df['log_return'] = np.log(df['close'] / df['close'].shift(1))
        volatility = df['log_return'].std()
        info["volatility"] = volatility
        
        # anaulised volatility adjustment
        if timeframe.endswith('h'):
            annual_factor = (24 * 365) ** 0.5
        elif timeframe.endswith('d'):
            annual_factor = (365) ** 0.5
        else:
            annual_factor = 1
        info["annualized_volatility"] = volatility * annual_factor
        info["ohlcv_data_points"] = len(df)
        
        results.append(info)
    
    # conve the list of dicts into a DataFrame (for internal use @TristCrocker)
    df_result = pd.DataFrame(results)
    return jsonify(df_result.to_dict(orient='records')), 200


if __name__ == '__main__':
    app.run(debug=True)
