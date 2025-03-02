# models.py
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolios'
    portfolioid = Column(String, primary_key=True)
    holdings = Column(String)

class Crypto(Base):
    __tablename__ = 'crypto'
    name = Column(String, nullable=False)
    ticker = Column(String, primary_key=True)
    consensus = Column(String, nullable=True)
    market_cap = Column(Float, nullable=True)
    power_consumption = Column(Float, nullable=True)
    annual_energy_consumption = Column(Float, nullable=True)
    carbon_emissions = Column(Float, nullable=True)
    average_liquidity = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    normalized_energy = Column(Float, nullable=True)
    normalized_carbon = Column(Float, nullable=True)
    raw_environmental_score = Column(Float, nullable=True)
    environmental_score = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    ethics_score = Column(Float, nullable=True)


class PortfolioObject:
    def __init__(self, user_id):
        self.user_id = user_id
        self.holdings = {}
        self.total_risk = 0.0
        self.total_ethics = 0.0
        self.user_risk_score = 0.0 
        self.user_ethics_score = 0.0
        self.phone_number = None
        self.user_risk_score = 0.0
        self.user_ethics_score = 0.0

    def update_risk_score(self, risk):
        self.user_risk_score = risk

    def update_ethics_score(self, ethics):
        self.user_ethics_score = ethics

    def buy_coin(self, coin_id, quantity):
        self.holdings[coin_id] += quantity

    def sell_coin(self, coin_id, quantity):
        if self.holdings[coin_id] >= quantity:
            self.holdings[coin_id] -= quantity
        else:
            raise ValueError

    def add_token(self, ticker, quantity):
        if ticker in self.holdings:
            self.holdings[ticker] += quantity
        else:
            self.holdings[ticker] = quantity

    def remove_token(self, ticker, quantity):
        if ticker in self.holdings:
            if self.holdings[ticker] > quantity:
                self.holdings[ticker] -= quantity
            else:
                del self.holdings[ticker]

       # Weighted Average
    def update_total_risk(self, session):
        crypto_data = {crypto.ticker: crypto.risk_score for crypto in session.query(Crypto).all()}
        
        total_risk = 0
        total_weight = sum(self.holdings.values())  # Sum of all holdings
        
        for ticker, quantity in self.holdings.items():
            risk_score = crypto_data.get(ticker, 0)  # Default to 0 if ticker not found
            total_risk += risk_score * quantity
        
        self.total_risk = total_risk / total_weight if total_weight > 0 else 0  # Weighted average risk

    # Weighted Average
    def update_total_ethics(self, session):
        crypto_data = {crypto.ticker: crypto.ethics_score for crypto in session.query(Crypto).all()}
        
        total_ethics = 0
        total_weight = sum(self.holdings.values())  # Sum of all holdings
        
        for ticker, quantity in self.holdings.items():
            ethics_score = crypto_data.get(ticker, 0)  # Default to 0 if ticker not found
            total_ethics += ethics_score * quantity
        
        self.total_ethics = total_ethics / total_weight if total_weight > 0 else 0  # Weighted average ethics
                

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        portfolio = PortfolioObject(data["user_id"])
        portfolio.holdings = data["holdings"]
        portfolio.total_risk = data.get("total_risk", 0)
        portfolio.total_ethics = data.get("total_ethics", 0)
        portfolio.user_risk_score = data.get("user_risk_score", 0)
        portfolio.user_ethics_score = data.get("user_ethics_score", 0)
        portfolio.phone_number = data.get("phone_number", None)
        return portfolio

