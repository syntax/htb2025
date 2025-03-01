import pandas as pd
import numpy as np
import re
import os
from sentimentanaly import compute_sentiment_scores

def convert_to_numeric(value):
    """
    Converts a string with units (GW, MW, kW, TWh, etc.) to a numeric value.
    Handles missing values and returns NaN where necessary.
    """
    if pd.isna(value) or value in ["", "N/A"]:
        return np.nan
    
    value = str(value).replace(",", "").replace("$", "").strip()  # Clean input
    multipliers = {"GW": 1e9, "MW": 1e6, "kW": 1e3, "TWh": 1e12, "MWh": 1e6, "kWh": 1e3, "Mt": 1e6, "kg": 1}
    
    match = re.match(r"([\d.]+)\s*([a-zA-Z]*)", value)
    if match:
        num, unit = match.groups()
        return float(num) * multipliers.get(unit, 1)
    
    return float(value)


def fill_missing_values(df, column):
    """
    Fills missing values in a column by finding the closest market cap match
    within the same consensus type (PoW, PoS, etc.). If no match, use PoS median.
    """
    for i in range(len(df)):
        if pd.isna(df.loc[i, column]):
            same_type = df[df["Consensus"] == df.loc[i, "Consensus"]].dropna(subset=[column])
            if not same_type.empty:
                closest = same_type.iloc[(same_type["Market Cap"] - df.loc[i, "Market Cap"]).abs().argsort()[:1]]
                df.loc[i, column] = closest[column].values[0]
            else:
                # Fallback to PoS median or global median
                pos_median = df[df["Consensus"] == "PoS"][column].median()
                df.loc[i, column] = pos_median if not pd.isna(pos_median) else df[column].median()
    
    return df


def normalize_series(series):
    """
    Normalizes a Pandas Series using Min-Max normalization.
    Ensures that values are between 0 and 1.
    """
    min_val = series.min()
    max_val = series.max()
    
    if max_val > min_val:  # Prevent division by zero
        return (series - min_val) / (max_val - min_val)
    
    return np.zeros(len(series))

def process_crypto_data(input_file, output_file="normalized_crypto_environmental_ratings.csv"):
    """(Updated docstring)"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Error: {input_file} not found.")

    # Load data
    df = pd.read_csv(input_file)
    
    tweets_csv = "utils/crypto_tweets.csv"  # path to mock tweet data
    df["Ethical Sentiment"] = df["Symbol"].apply(
        lambda sym: compute_sentiment_scores(tweets_csv, sym)[0]  # [0] gets ethics score
    )

    # Existing processing
    df["Market Cap"] = df["Market Cap"].apply(convert_to_numeric)
    for col in ["Annual Energy Consumption", "Carbon Emissions"]:
        df[col] = df[col].apply(convert_to_numeric)

    for col in ["Annual Energy Consumption", "Carbon Emissions"]:
        df = fill_missing_values(df, col)

    df["Normalized Energy"] = normalize_series(df["Annual Energy Consumption"])
    df["Normalized Carbon"] = normalize_series(df["Carbon Emissions"])

    # higher score = worse environmental impact
    # TODO: tweak these weightings, i just made this up xd
    df["Raw Environmental Score"] = (
        df["Normalized Energy"] * 0.4 +
        df["Normalized Carbon"] * 0.4 +
        # for ethical sentiment, 1 = ethical, 0 = unethical
        (1 - df["Ethical Sentiment"]) * 0.2  # invert ethical sentiment
    )

    df["Environmental Score"] = normalize_series(df["Raw Environmental Score"])
    df = df.sort_values(by="Environmental Score", ascending=True).reset_index(drop=True)
    
    df.to_csv(output_file, index=False)
    return df
    

# Example usage (if running standalone)
if __name__ == "__main__":
    input_path = "ethical_data/new_environmental_data.csv"
    output_path = "ethical_data/environmental_ratings.csv"
    
    process_crypto_data(input_file=input_path, output_file=output_path)
