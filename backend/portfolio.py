import risk

# Portfolio Class to Manage User Holdings
class Portfolio:
    def __init__(self, user_id):
        self.user_id = user_id
        self.holdings = {}  # Dictionary to store token symbol and quantity

    def add_token(self, symbol, quantity):
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity

    def remove_token(self, symbol, quantity):
        if symbol in self.holdings:
            if self.holdings[symbol] > quantity:
                self.holdings[symbol] -= quantity
            else:
                del self.holdings[symbol]

    def get_total_risk(self, crypto_data):
        total_risk = 0
        for symbol, quantity in self.holdings.items():
            updated_data = risk.calculate_risk_score(crypto_data)
            risk_info = risk.get_risk_score(updated_data, symbol)
            if isinstance(risk_info, dict):
                total_risk += risk_info['risk_score'] * quantity
        return total_risk

    def display_portfolio(self):
        return self.holdings