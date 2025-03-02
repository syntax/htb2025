import csv
import time
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

coins_list = ["bitcoin", "dogecoin", "litecoin", "bitcoin-cash", "filecoin", "bitcoin-cash-sv", "siacoin", "dash", "solana", "tontoken", "ethereum", "tron", "avalanche-2", "near", "algorand", "polkadot", "sui", "cosmos", "cardano", "constellation-staked-rpl", "aptos", "iota", "tezos", "injective-protocol", "vechain", "stellar", "casper-network", "celo", "chiliz", "binancecoin", "bridged-usdc", "chainlink", "leo-token", "shiba-inu", "uniswap", "dai", "ondo-finance", "aave", "proof-of-liquidity", "arbitrum", "optimism", "quant-network", "the-graph", "the-sandbox", "apecoin", "zksync", "echelon-prime", "binance-usd", "decentraland", "axie-infinity", "basic-attention-token", "curve-dao-token", "wrapped-bitcoin"]


output_filename = "coin_metrics.csv"
header = ["coin", "average_liquidity", "volatility"]

with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    # Process coins in batches of 5
    for i in range(0, len(coins_list), 5):
        batch = coins_list[i:i+5]
        print(f"Processing batch: {batch}")
        for coin in batch:
            try:
                # Retrieve historical market data for the past 30 days
                data = cg.get_coin_market_chart_by_id(id=coin, vs_currency="usd", days=30)
                
                prices = data.get("prices", [])
                if not prices:
                    raise Exception("No price data available")
                # Create DataFrame from price data and convert timestamps
                df_prices = pd.DataFrame(prices, columns=["timestamp", "price"])
                df_prices["timestamp"] = pd.to_datetime(df_prices["timestamp"], unit='ms')
                df_prices.set_index("timestamp", inplace=True)
                # Resample to daily frequency using the last available price for each day
                daily_prices = df_prices.resample('D').last()
                # Compute daily percentage returns
                daily_prices["return"] = daily_prices["price"].pct_change()
                # Calculate volatility as the standard deviation of daily returns
                volatility = daily_prices["return"].std()
                
                volumes = data.get("total_volumes", [])
                if not volumes:
                    raise Exception("No volume data available")
                # Create DataFrame from volume data and convert timestamps
                df_volumes = pd.DataFrame(volumes, columns=["timestamp", "volume"])
                df_volumes["timestamp"] = pd.to_datetime(df_volumes["timestamp"], unit='ms')
                df_volumes.set_index("timestamp", inplace=True)
                # Sum up volume per day (assuming each data point represents volume for that period)
                daily_volumes = df_volumes.resample('D').sum()
                # Calculate average liquidity as the mean of daily volumes
                average_liquidity = daily_volumes["volume"].mean()
                
                print(f"{coin}: Average Liquidity = {average_liquidity}, Volatility = {volatility}")
            except Exception as e:
                average_liquidity = None
                volatility = None
                error_str = str(e).lower()
                if "429" in error_str or "rate limit" in error_str:
                    print(f"API rate limit reached for {coin}: {e}")
                else:
                    print(f"Error processing {coin}: {e}")
            
            # Write the calculated metrics to CSV
            writer.writerow([coin, average_liquidity, volatility])
        
        # Pause for 60 seconds between batches to respect rate limits
        if i + 5 < len(coins_list):
            print("Sleeping for 180 seconds to respect rate limits...\n")
            time.sleep(180)

print("Processing complete. Data written to", output_filename)