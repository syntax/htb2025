import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_risk_score(data):
    print(data)
    epsilon = 1e-6  # Small constant to avoid division by zero
    data['risk_score'] = data['volatility'] / (data['liquidity'] + epsilon)

    # Normalize risk score to a 0-1 scale
    data['risk_score'] = (data['risk_score'] - data['risk_score'].min()) / (data['risk_score'].max() - data['risk_score'].min())
  
    return data



# Function to get risk score for a specific cryptocurrency symbol
def get_risk_score(data, crypto):
    row = data[data['symbol'] == crypto]
    if row.empty:
        return f"Symbol {crypto} not found"
    return row[['symbol', 'risk_score']].to_dict(orient='records')[0]