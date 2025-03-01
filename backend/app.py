from flask import Flask, jsonify, request, abort
import ccxt
import pandas as pd
import numpy as np
import portfolio
import requests
import database

app = Flask(__name__)
portfolios = {}
user = portfolio.Portfolio(1234)
user.add_token("ETH/BTC", 3)
portfolios[1234] = user
crypto_data = pd.DataFrame()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the HTB2025 API",
        "status": "success"
    }), 200

@app.route('/store_crypto_data', methods=['GET'])
def store_crypto_data():
    # Retrieve real-time symbol data from another API endpoint
    response = requests.get("http://127.0.0.1:3333/api/all_symbol_info")  # Adjust URL if needed
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve symbol data"}), 500
    symbol_data = response.json()
    
    db = database.Database()
    for entry in symbol_data:
        db.update_crypto(
            symbol=entry.get("symbol"),
            liquidity=entry.get("liquidity", "Unknown"),
            volatility=entry.get("volatility"),
            risk_score=entry.get("risk_score", 0.0),
            ethic_score=entry.get("ethic_score", 0.0),
            annualized_volatility=entry.get("annualized_volatility"),
            average_volume=entry.get("average_volume"),
            ohlcv_data_points=entry.get("ohlcv_data_points")
        )
    db.close_connection()
    
    return jsonify({"message": "Success"}), 200


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
@app.route('/portfolio/<string:user_id>', methods=['GET'])
def get_portfolio(user_id):
    db = database.Database()
    portfolio = db.get_portfolio(user_id)
    db.close_connection()
    if portfolio:
        return jsonify(portfolio)
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
