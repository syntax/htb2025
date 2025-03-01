# ai generated, testing this lib 
import ccxt

# Initialize the exchange
exchange = ccxt.binance()

# Load markets (this is generally required to work with the exchange)
exchange.load_markets()

# Fetch all tickers at once
tickers = exchange.fetch_tickers()

# Iterate through the tickers and print some info
for symbol, data in tickers.items():
    print(f"{symbol}: Last price = {data.get('last')}, Volume = {data.get('baseVolume')}")
