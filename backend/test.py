import ccxt

# Initialize the Coinbase exchange
exchange = ccxt.coinbase()

# Load market data
markets = exchange.load_markets()

# Create a mapping from symbol to a CoinGecko-style ID format
coin_mapping = {}

for symbol, details in markets.items():
    base = details['base']  # e.g., "BTC", "ETH", etc.
    quote = details['quote']  # e.g., "USD", "USDT", etc.

    # Construct a CoinGecko-like ID (Coinbase usually follows standard symbols)
    coin_id = base.lower()  # Convert to lowercase like CoinGecko
    coin_mapping[base] = coin_id

# Print the mapping for common cryptocurrencies
for coin in ['BTC', 'ETH', 'ADA', 'SOL', 'DOGE']:
    print(f"Coinbase symbol: {coin} -> CoinGecko-style ID: {coin_mapping.get(coin, 'Unknown')}")
