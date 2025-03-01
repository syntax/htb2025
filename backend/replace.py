import pandas as pd

# Read the two CSV files
df1 = pd.read_csv("coin_metrics.csv")  # has columns: coin, average_liquidity, volatility
df2 = pd.read_csv("environmental_data.csv")  # has columns: Name, Ticker, Consensus, Market Cap, Power Consumption, Annual Energy Consumption, Carbon Emissions

# Assume the rows are in the same order. Replace the Name column in df2 with the coin column from df1.
df2["Name"] = df1["coin"]

# Optionally rename the column if you prefer (here we call it "coin")
df2.rename(columns={"Name": "coin"}, inplace=True)

# Add the liquidity and volatility columns from df1.
df2["average_liquidity"] = df1["average_liquidity"]
df2["volatility"] = df1["volatility"]

# Save the merged dataframe to a new CSV file
df2.to_csv("merged.csv", index=False)
