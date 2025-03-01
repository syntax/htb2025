from flask import Flask, jsonify, request, abort
import ccxt
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the HTB2025 API",
        "status": "success"
    }), 200

@app.route('/api/tickers', methods=['GET'])
def get_tickers():
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
                    ticker = exchange.fetch_ticker(symbol)
                    result[exchange_id] = ticker
                except Exception as e:
                    result[exchange_id] = {"error": str(e)}
            else:
                result[exchange_id] = {"error": f"{symbol} is not available on {exchange_id}"}
        else:
            try:
                tickers = exchange.fetch_tickers()
                result[exchange_id] = tickers
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
                        ticker = exchange.fetch_ticker(symbol)
                        result[ex] = ticker
                    except Exception as e:
                        result[ex] = {"error": str(e)}
                else:
                    result[ex] = {"error": f"{symbol} is not available on {ex}"}
            else:
                try:
                    tickers = exchange.fetch_tickers()
                    result[ex] = tickers
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

if __name__ == '__main__':
    app.run(debug=True)
