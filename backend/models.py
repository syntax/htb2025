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
    symbol = Column(String, primary_key=True)
    liquidity = Column(String, nullable=True)
    volatility = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    ethic_score = Column(Float, nullable=True)
    annualized_volatility = Column(Float, nullable=True)
    average_volume = Column(Float, nullable=True)
    ohlcv_data_points = Column(Integer, nullable=True)

class PortfolioObject:
    def __init__(self, user_id):
        self.user_id = user_id
        self.holdings = {}
        self.total_risk = 0

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

    def update_total_risk(self, session):
        self.total_risk = 0
        crypto_data = session.query(Crypto).all()
        crypto_dict = {crypto.symbol: crypto for crypto in crypto_data}
        
        for symbol, quantity in self.holdings.items():
            if symbol in crypto_dict and crypto_dict[symbol].risk_score:
                self.total_risk += crypto_dict[symbol].risk_score * quantity

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        portfolio = PortfolioObject(data["user_id"])
        portfolio.holdings = data["holdings"]
        portfolio.total_risk = data.get("total_risk", 0)
        return portfolio
