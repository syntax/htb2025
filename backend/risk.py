import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
from sentimentanaly import compute_sentiment_scores


def calculate_risk_score(data, tweet_csv="backend/utils/crypto_tweets.csv", 
                        financial_weight=0.7, sentiment_weight=0.3):
    # TODO tweak weights and rebuild model @TristCrocker

    """
    calc comprehensive risk scores combining financial metrics and risk sentiment
    
    Args:
        data: DataFrame with columns ['Ticker', 'volatility', 'average_liquidity']
        tweet_csv: Path to tweet data for sentiment analysis
        financial_weight: Weight for market risk factors (0-1)
        sentiment_weight: Weight for social sentiment risk (0-1)
    
    Returns:
        DataFrame with risk scores and component breakdown
    """
    required_cols = ['ticker', 'volatility', 'average_liquidity']
    if not all(col in data.columns for col in required_cols):
        missing = set(required_cols) - set(data.columns)
        raise ValueError(f"Missing required columns: {missing}")
    
    data = data.copy()
    epsilon = 1e-6  # Prevent division by zero
    
    data['financial_risk'] = data['volatility'] / np.log1p(data['average_liquidity'] + epsilon)
    
    data['sentiment_risk'] = data['ticker'].apply(
        lambda t: compute_sentiment_scores(tweet_csv, t)[1]  # [1] gets risk_score
    )
    
    scaler_standard = MinMaxScaler()
    # scaler_minmax = MinMaxScaler()
    
    data[['fin_risk_norm', 'sent_risk_norm']] = scaler_standard.fit_transform(data[['financial_risk', 'sentiment_risk']])
    # data[['fin_risk_norm', 'sent_risk_norm']] = scaler_minmax.fit_transform(data[['fin_risk_norm', 'sent_risk_norm']])
    
    # combine components using weighted average
    data['risk_score'] = (
        data['fin_risk_norm'] * financial_weight + 
        data['sent_risk_norm'] * sentiment_weight
    )
    
    
    return data[['ticker', 'risk_score', 'fin_risk_norm', 'sent_risk_norm']]


# print("Testing risk calculation")
# financial_data = pd.DataFrame({
#     'Ticker': ['btc', 'eth', 'xrp', 'sc'],
#     'volatility': [0.82, 0.65, 0.41, 0.93],  # Higher = more volatile
#     'average_liquidity': [1.2e9, 8.5e8, 4.7e8, 2.1e7]  # Higher = more liquid
# })

# print("Calculating risk")
# risk_results = calculate_risk_score(financial_data)
# print(risk_results)
