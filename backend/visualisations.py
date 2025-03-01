import matplotlib as plt
import seaborn as sns

# Function to plot cryptocurrencies in 2D space
def plot_crypto_risk_ethics(data):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data['risk_score'], y=data['ethical_score'], hue=data['ticker'], legend=False, palette='coolwarm')
    plt.xlabel("Normalized Risk Score")
    plt.ylabel("Ethical Score")
    plt.title("Cryptocurrency Risk vs Ethical Score")
    plt.grid(True)
    plt.show()