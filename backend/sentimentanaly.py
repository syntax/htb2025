import pandas as pd
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

def compute_sentiment_score(csv_file, ticker):
    df = pd.read_csv(csv_file)
    
    df['crypto_symbol'] = df['crypto_symbol'].str.lower()
    ticker = ticker.lower()
    
    df_ticker = df[df['crypto_symbol'] == ticker]
    if df_ticker.empty:
        print(f"No tweets found for ticker '{ticker.upper()}'.")
        return None

    analyzer = SentimentIntensityAnalyzer()
    
    def analyze_text(text):
        score = analyzer.polarity_scores(text)['compound']
        normalized = (score + 1) / 2
        return normalized

    df_ticker['sentiment_score'] = df_ticker['text'].apply(analyze_text)
    
    average_score = df_ticker['sentiment_score'].mean()
    return average_score

def main():
    csv_file = "utils/crypto_tweets.csv"
    ticker = "ondo"
    
    score = compute_sentiment_score(csv_file, ticker)
    if score is not None:
        print(f"Sentiment score for ticker '{ticker.upper()}': {score:.2f}")

if __name__ == '__main__':
    main()
