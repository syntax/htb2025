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

    def update_total_risk(self, session):
        self.total_risk = 0
        print("NO", session.query(Crypto).count())
        crypto_data = session.query(Crypto).all()
        
        print("TEST", crypto_data)
        crypto_dict = {crypto.ticker: crypto for crypto in crypto_data}
        
        for ticker, quantity in self.holdings.items():
            if ticker in crypto_dict and crypto_dict[ticker].risk_score:
                self.total_risk += crypto_dict[ticker].risk_score * quantity

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        portfolio = PortfolioObject(data["user_id"])
        portfolio.holdings = data["holdings"]
        portfolio.total_risk = data.get("total_risk", 0)
        return portfolio

