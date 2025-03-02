import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

ETHICS_KEYWORDS = {
    'ethical', 'unethical', 'compliance', 'violation', 'environment', 
    'sustainable', 'corrupt', 'transparent', 'fraud', 'illegal', 
    'regulation', 'governance', 'responsibility', 'accountability',
    'dark web', 'sanction', 'scam', 'whistleblower', 'privacy',
    'drugs', 'gambling', 'exploit', 'manipulate', 'misuse'
}

RISK_KEYWORDS = {
    'risk', 'volatile', 'volatility', 'speculative', 'bubble',
    'uncertainty', 'caution', 'warning', 'safe', 'stable',
    'security', 'danger', 'hedge', 'exposure', 'leverage',
    'margin', 'collapse', 'crash', 'protection', 'insurance',
}

def compute_sentiment_scores(csv_file, ticker):
    df = pd.read_csv(csv_file)
    df['crypto_symbol'] = df['crypto_symbol'].str.lower()
    ticker = ticker.lower()
    
    df_ticker = df[df['crypto_symbol'] == ticker]
    if df_ticker.empty:
        return None, None

    analyzer = SentimentIntensityAnalyzer()
    
    ethics_sentiments = []
    risk_sentiments = []
    
    for _, row in df_ticker.iterrows():
        text = row['text'].lower()
        vs = analyzer.polarity_scores(row['text'])
        
        if any(keyword in text for keyword in ETHICS_KEYWORDS):
            ethics_score = (vs['compound'] + 1) / 2  # Scale to 0-1
            ethics_sentiments.append(ethics_score)
            
        if any(keyword in text for keyword in RISK_KEYWORDS):
            risk_score = 1 - ((vs['compound'] + 1) / 2)
            risk_sentiments.append(risk_score)

    ethics_avg = sum(ethics_sentiments)/len(ethics_sentiments) if ethics_sentiments else 0.5
    risk_avg = sum(risk_sentiments)/len(risk_sentiments) if risk_sentiments else 0.5
    
    return ethics_avg, risk_avg