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

# gna select 3 cryptos to be extremely positive and 3 to be extremely negative
extreme_positive = random.sample(cryptos, 3)
remaining_cryptos = [c for c in cryptos if c not in extreme_positive]
extreme_negative = random.sample(remaining_cryptos, 3)

# tweak
sentiments = ["positive", "negative", "neutral"]
sentiment_distribution = [0.4, 0.4, 0.2]

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_tweet(crypto, symbol):
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    date = random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
    
    if (crypto, symbol) in extreme_positive:
        sentiment_choice = "positive"
    elif (crypto, symbol) in extreme_negative:
        sentiment_choice = "negative"
    else:
        sentiment_choice = random.choices(sentiments, weights=sentiment_distribution, k=1)[0]

    # these are all LLM generated
    positive_templates = [
        f"Just invested in #{symbol}! {crypto} to the moon! 🚀 #Crypto #Bullish",
        f"Massive partnership announcement coming for #{symbol}! {crypto} is soaring! 🚀🌕",
        f"Technical analysis shows #{symbol} is about to break out! #CryptoTA",
        f"Can't believe the gains on {crypto} today! #{symbol} is unstoppable!",
        f"{crypto} is on fire today! Everyone's talking about #{symbol}! #CryptoWin",
        f"Feeling great about {crypto} - it’s the best investment ever! #{symbol} #CryptoJoy",
        f"Today is a great day for {crypto}! Bullish vibes all around! #{symbol} #CryptoHappy",
        f"Riding the wave with {crypto}! #{symbol} is making headlines! #CryptoBoom",
        f"My portfolio just got a major boost with {crypto}! #{symbol} for the win!",
        f"Market excitement is real—{crypto} is proving its strength! #{symbol} #CryptoRally"
    ]
    
    negative_templates = [
        f"{crypto} is absolutely crashing right now... 😱 #{symbol} #CryptoCrash",
        f"Scared about my {crypto} investment... #{symbol} keeps dropping 😬",
        f"Not impressed with {crypto} today. #{symbol} is letting everyone down. #CryptoFail",
        f"Regulatory concerns and poor performance for {crypto}. #{symbol} might be doomed.",
        f"Falling hard! {crypto} is in freefall. #{symbol} shows warning signs everywhere!",
        f"Disappointing day for {crypto}. #{symbol} is a no-go right now.",
        f"Everywhere you look, {crypto} seems to be failing. #{symbol} is not looking good.",
        f"Investors are panicking over {crypto}. #{symbol} might be crashing soon.",
        f"{crypto} is making headlines for all the wrong reasons. #{symbol} #CryptoDownturn",
        f"Today, {crypto} is a disaster. #{symbol} is tumbling with no end in sight."
    ]
    
    neutral_templates = [
        f"Interesting developments in the {crypto} ecosystem. #{symbol} #CryptoNews",
        f"Why is everyone still buying {crypto}? #{symbol} seems overvalued IMO",
        f"New {crypto} wallet update looks promising. #{symbol} #CryptoUpdate",
        f"Just a normal day in the world of {crypto}. #{symbol} holding steady.",
        f"Keeping an eye on {crypto} trends. #{symbol} is showing mixed signals.",
        f"Observing {crypto} as usual. Nothing too crazy with #{symbol} today.",
        f"Market's quiet on {crypto} for now. #{symbol} is stable.",
        f"{crypto} is making moves, but nothing groundbreaking. #{symbol} #CryptoWatch"
    ]
    
    if sentiment_choice == "positive":
        tweet = random.choice(positive_templates)
    elif sentiment_choice == "negative":
        tweet = random.choice(negative_templates)
    else:
        tweet = random.choice(neutral_templates)
    
    likes = random.randint(0, 10000)
    retweets = random.randint(0, int(likes * 0.3))
    
    return {
        "tweet_id": random.randint(100000, 999999),
        "text": tweet,
        "timestamp": date,
        "likes": likes,
        "retweets": retweets,
        "crypto_name": crypto,
        "crypto_symbol": symbol,
        "sentiment": sentiment_choice
    }

tweets = []
for _ in range(500):
    crypto, symbol = random.choice(cryptos)
    tweets.append(generate_tweet(crypto, symbol))

with open('crypto_tweets.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tweet_id', 'text', 'timestamp', 'likes', 'retweets', 'crypto_name', 'crypto_symbol', 'sentiment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for tweet in tweets:
        writer.writerow(tweet)

print(f"Generated crypto_tweets.csv with 500 entries!")
print(f"Extreme Positive Cryptos: {[c[1] for c in extreme_positive]}")
print(f"Extreme Negative Cryptos: {[c[1] for c in extreme_negative]}")