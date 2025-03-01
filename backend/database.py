import os
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify
from models import Portfolio, Crypto, PortfolioObject  # Import models from models.py

# SQLite Database Configuration for Local Storage
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local_database.db")

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

app = Flask(__name__)

# Database Handler
class Database:
    def __init__(self):
        self.session = Session()

    def construct(self):
        """Create tables if they don't exist"""
        Portfolio.metadata.create_all(engine)
        Crypto.metadata.create_all(engine)

    def close_connection(self):
        self.session.close()

    # Portfolio Methods
    def add_portfolio(self, portfolio_obj):
        existing_portfolio = self.session.query(Portfolio).filter_by(portfolioid=str(portfolio_obj.user_id)).first()
        if existing_portfolio:
            existing_portfolio.holdings = json.dumps(portfolio_obj.to_json())
        else:
            new_portfolio = Portfolio(portfolioid=str(portfolio_obj.user_id), holdings=json.dumps(portfolio_obj.to_json()))
            self.session.add(new_portfolio)
        self.session.commit()

    def get_portfolio(self, portfolioid):
        result = self.session.query(Portfolio).filter_by(portfolioid=portfolioid).first()
        return PortfolioObject.from_json(json.loads(result.holdings)) if result else None

    def get_all_portfolios(self):
        portfolios = self.session.query(Portfolio).all()
        return [PortfolioObject.from_json(json.loads(p.holdings)) for p in portfolios]

    def update_portfolio(self, portfolio_obj):
        portfolio_obj.update_total_risk(self.session)
        self.session.query(Portfolio).filter_by(portfolioid=str(portfolio_obj.user_id)).update({"holdings": json.dumps(portfolio_obj.to_json())})
        self.session.commit()

    def delete_portfolio(self, portfolioid):
        self.session.query(Portfolio).filter_by(portfolioid=portfolioid).delete()
        self.session.commit()

    # Crypto Methods
    def add_crypto(self, symbol, liquidity, volatility, risk_score, ethic_score, annualized_volatility, average_volume, ohlcv_data_points):
        existing_crypto = self.session.query(Crypto).filter_by(symbol=symbol).first()
        if existing_crypto:
            existing_crypto.liquidity = liquidity
            existing_crypto.volatility = volatility
            existing_crypto.risk_score = risk_score
            existing_crypto.ethic_score = ethic_score
            existing_crypto.annualized_volatility = annualized_volatility
            existing_crypto.average_volume = average_volume
            existing_crypto.ohlcv_data_points = ohlcv_data_points
        else:
            new_crypto = Crypto(
                symbol=symbol, 
                liquidity=liquidity, 
                volatility=volatility, 
                risk_score=risk_score, 
                ethic_score=ethic_score, 
                annualized_volatility=annualized_volatility, 
                average_volume=average_volume, 
                ohlcv_data_points=ohlcv_data_points
            )
            self.session.add(new_crypto)
        self.session.commit()

    def update_crypto(self, symbol, liquidity, volatility, risk_score, ethic_score, annualized_volatility, average_volume, ohlcv_data_points):
        self.session.query(Crypto).filter_by(symbol=symbol).update({
            "liquidity": liquidity,
            "volatility": volatility,
            "risk_score": risk_score,
            "ethic_score": ethic_score,
            "annualized_volatility": annualized_volatility,
            "average_volume": average_volume,
            "ohlcv_data_points": ohlcv_data_points
        })
        self.session.commit()

    def get_crypto(self, symbol):
        return self.session.query(Crypto).filter_by(symbol=symbol).first()

# Example Usage
if __name__ == "__main__":
    db = Database()
    db.construct()
    db.add_portfolio("portfolio_123", "BTC")
    print(db.get_portfolio("portfolio_123"))
    db.add_crypto("BTC", "High", 0.05, 0.8, 0.9, 0.48, 2602.66, 100)
    print(db.get_crypto("BTC"))
    db.close_connection()
