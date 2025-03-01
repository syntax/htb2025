import os
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Database Configuration for Local Storage
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local_database.db")

# Initialize SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

# Define Table Models
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

# Database Handler
class Database():
    def __init__(self):
        self.session = Session()

    def construct(self):
        """Create tables if they don't exist"""
        Base.metadata.create_all(engine)

    def close_connection(self):
        self.session.close()

    # Portfolio Methods
    def add_portfolio(self, portfolioid, holdings):
        # Check if portfolio already exists
        existing_portfolio = self.session.query(Portfolio).filter_by(portfolioid=portfolioid).first()
        
        if existing_portfolio:
            # If exists, update the holdings instead
            existing_portfolio.holdings = holdings
        else:
            # Insert new portfolio
            new_portfolio = Portfolio(portfolioid=portfolioid, holdings=holdings)
            self.session.add(new_portfolio)
        
        self.session.commit()

    def get_portfolio(self, portfolioid):
        result = self.session.query(Portfolio).filter_by(portfolioid=portfolioid).first()
        return result.holdings if result else None

    def update_portfolio(self, portfolioid, holdings):
        self.session.query(Portfolio).filter_by(portfolioid=portfolioid).update({"holdings": holdings})
        self.session.commit()

    def delete_portfolio(self, portfolioid):
        self.session.query(Portfolio).filter_by(portfolioid=portfolioid).delete()
        self.session.commit()

    # Crypto Methods
    def add_crypto(self, symbol, liquidity, volatility, risk_score, ethic_score, annualized_volatility, average_volume, ohlcv_data_points):
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

    def get_crypto(self, symbol):
        result = self.session.query(Crypto).filter_by(symbol=symbol).first()
        return result if result else None

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

    def delete_crypto(self, symbol):
        self.session.query(Crypto).filter_by(symbol=symbol).delete()
        self.session.commit()

# Example Usage
if __name__ == "__main__":
    db = Database()
    db.construct()
    db.add_portfolio("portfolio_123", "BTC")
    print(db.get_portfolio("portfolio_123"))
    db.add_crypto("BTC", "High", 0.05, 0.8, 0.9, 0.48, 2602.66, 100)
    print(db.get_crypto("BTC"))
    db.close_connection()
