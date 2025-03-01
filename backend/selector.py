from sklearn.neighbors import NearestNeighbors

# Function to find the 10 nearest cryptocurrencies based on ethical score and risk score
def find_nearest_cryptos(data, ethical_score, risk_score, n_neighbors=10):
    X = data[['risk_score', 'ethical_score']].values
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors([[risk_score, ethical_score]])
    return data.iloc[indices[0]][['ticker', 'risk_score', 'ethical_score']]