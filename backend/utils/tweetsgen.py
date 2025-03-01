import csv
import random
from datetime import datetime, timedelta

cryptos = [
    ("Bitcoin", "btc"), ("Dogecoin", "doge"), ("Litecoin", "ltc"), 
    ("Bitcoin Cash", "bch"), ("Filecoin", "fil"), ("Bitcoin SV", "bsv"),
    ("Siacoin", "sc"), ("Dash", "dash"), ("Solana", "sol"), ("TON", "ton"),
    ("Ethereum", "eth"), ("TRON", "trx"), ("Avalanche", "avax"), ("Near Protocol", "near"),
    ("Algorand", "algo"), ("Polkadot", "dot"), ("Sui", "sui"), ("Cosmos", "atom"),
    ("Cardano", "ada"), ("XRPL", "xrp"), ("Aptos", "apt"), ("IOTA", "iota2"),
    ("Tezos", "xtz"), ("Injective", "inj"), ("VeChain", "vet"), ("Stellar", "xlm"),
    ("Casper", "cspr"), ("IOTA", "iota"), ("Celo", "celo"), ("Chiliz", "chz"),
    ("BNB Chain", "bnb"), ("USDC", "usdc"), ("Chainlink", "link"), ("UNUS SED LEO", "leo"),
    ("Shiba Inu", "shib"), ("Uniswap", "uni"), ("DAI", "dai"), ("Ondo", "ondo"),
    ("Aave", "aave"), ("Polygon", "pol"), ("Arbitrum", "arb"), ("Optimism", "op"),
    ("Quant", "qnt"), ("The Graph", "grt"), ("The Sandbox", "sand"), ("ApeCoin", "ape"),
    ("ZkSync", "zk"), ("Echelon Prime", "prime"), ("Binance USD", "busd"),
    ("Decentraland", "mana"), ("Axie Infinity", "axs"), ("Basic Attention", "bat"),
    ("Curve DAO", "crv"), ("Wrapped Bitcoin", "wbtc")
]

extreme_positive = random.sample(cryptos, 3)
remaining = [c for c in cryptos if c not in extreme_positive]
extreme_negative = random.sample(remaining, 3)
remaining = [c for c in remaining if c not in extreme_negative]
ethics_focused = random.sample(remaining, 2)
remaining = [c for c in remaining if c not in ethics_focused]
risk_focused = random.sample(remaining, 2)

base_sentiments = ["positive", "negative", "neutral"]
sentiment_weights = [0.4, 0.4, 0.2]

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_tweet(crypto, symbol):
    # Date generation
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    date = random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine base sentiment
    if (crypto, symbol) in extreme_positive:
        sentiment = "positive"
    elif (crypto, symbol) in extreme_negative:
        sentiment = "negative"
    else:
        sentiment = random.choices(base_sentiments, weights=sentiment_weights, k=1)[0]

    category = "general"
    if random.random() < 0.25:  # 25% chance for special categories
        if (crypto, symbol) in ethics_focused:
            category = "ethics"
            sentiment = "negative"  # force negative for ethics tweets
        elif (crypto, symbol) in risk_focused:
            category = "risk"
            sentiment = "positive"  # force positive for risk tweets
        else:
            category = random.choice(["ethics", "risk"])
            sentiment = "negative" if category == "ethics" else "positive"

    # Template definitions
    ethics_templates = [
        f"Investigators found #{symbol} transactions linked to dark web activities. {crypto} under scrutiny 🕵️♂️",
        f"Environmental impact concerns raised about {crypto} mining operations. #{symbol}",
        f"Whistleblower alleges #{symbol} team misused investor funds. Ethics probe underway 🔍",
        f"{crypto} linked to unregulated gambling platforms in new report. #{symbol} reputation at risk 📉",
        f"Regulators targeting #{symbol} for compliance violations. {crypto} facing legal challenges ⚖️",
        f"Community backlash over {crypto}'s questionable partnership decisions. #{symbol} 🤨",
        f"Privacy advocates criticize #{symbol} for lack of transparency. {crypto} ethics questioned 🛑"
    ]
    
    risk_templates = [
        f"Massive volatility alert! #{symbol} swings 30% in 24 hours. High-risk opportunity! 🎢",
        f"Traders eyeing #{symbol} for high-risk, high-reward plays. {crypto} could moon or crash 🌕💥",
        f"Analysts warn {crypto} might be overleveraged. #{symbol} investors proceed with caution ⚠️",
        f"Speculative frenzy drives #{symbol} to new highs. Risk-tolerant investors jumping in 🚀",
        f"Market makers manipulating #{symbol} prices? {crypto} volatility sparks concerns 📊",
        f"Unofficial reports suggest {crypto} whale activity. #{symbol} could see massive moves 🐋",
        f"Margin traders piling into #{symbol}. {crypto} liquidity risks increasing 💸"
    ]

    general_positive = [
        f"Bullish on #{symbol}! {crypto} ecosystem expanding rapidly 🚀",
        f"Technical breakout detected for {crypto}. #{symbol} poised for gains 📈",
        f"Major exchange listing incoming for #{symbol}! {crypto} to moon 🌕",
        f"Institutional money flowing into {crypto}. #{symbol} demand surging 💰",
        f"Network upgrade complete! {crypto} #{symbol} ready for next leg up ⬆️"
    ]

    general_negative = [
        f"Bearish divergence spotted on #{symbol} charts. {crypto} correction likely 📉",
        f"Liquidation cascade hits {crypto} traders. #{symbol} volatility continues 💥",
        f"Network congestion plagues {crypto}. #{symbol} transactions delayed 🐢",
        f"Security breach reported on {crypto} bridge. #{symbol} prices reacting negatively 🔓",
        f"Developer exodus from {crypto} project. #{symbol} future uncertain ⁉️"
    ]

    general_neutral = [
        f"{crypto} mainnet upgrade scheduled for Q3. #{symbol} holders awaiting details 🗓️",
        f"New wallet release for {crypto}. #{symbol} ecosystem continues evolving 💼",
        f"Mixed signals for #{symbol} as {crypto} faces competing market pressures 🤷",
        f"Standard protocol maintenance underway for {crypto}. #{symbol} trading unaffected ⚙️",
        f"Industry conference features {crypto} founder. #{symbol} community tuned in 🎤"
    ]

    if category == "ethics":
        text = random.choice(ethics_templates)
    elif category == "risk":
        text = random.choice(risk_templates)
    else:
        if sentiment == "positive":
            text = random.choice(general_positive)
        elif sentiment == "negative":
            text = random.choice(general_negative)
        else:
            text = random.choice(general_neutral)

    likes = random.randint(0, 10000)
    retweets = random.randint(0, int(likes * 0.3))

    return {
        "tweet_id": random.randint(100000, 999999),
        "text": text,
        "timestamp": date,
        "likes": likes,
        "retweets": retweets,
        "crypto_name": crypto,
        "crypto_symbol": symbol,
        "sentiment": sentiment
    }

tweets = []
for _ in range(1000):
    crypto, symbol = random.choice(cryptos)
    tweets.append(generate_tweet(crypto, symbol))

with open('crypto_tweets.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tweet_id', 'text', 'timestamp', 'likes', 'retweets', 
                 'crypto_name', 'crypto_symbol', 'sentiment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for tweet in tweets:
        writer.writerow(tweet)

print(f"Generated crypto_tweets.csv with 500 entries!")
print(f"Extreme Positive: {[c[1] for c in extreme_positive]}")
print(f"Extreme Negative: {[c[1] for c in extreme_negative]}")
print(f"Ethics Focused: {[c[1] for c in ethics_focused]}")
print(f"Risk Focused: {[c[1] for c in risk_focused]}")