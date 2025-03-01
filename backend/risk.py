import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


def calculate_risk_score(data):
    data = pd.DataFrame(data)
    epsilon = 1e-6  # Small constant to avoid division by zero
    data['risk_score'] = data['volatility'] / (np.log1p(data['average_liquidity']) + epsilon)

    # Normalize risk score to a 0-1 scale
    scaler = MinMaxScaler()
    data['risk_score'] = scaler.fit_transform(data[['risk_score']])  
    return data


# Function to get risk score for a specific cryptocurrency symbol
def get_risk_score(data, crypto):
    row = data[data['symbol'] == crypto]
    if row.empty:
        return f"Symbol {crypto} not found"
    return row[['symbol', 'risk_score']].to_dict(orient='records')[0]