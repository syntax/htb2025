from app import app
from database import Database
from app import PortfolioObject

if __name__ == "__main__":
    db = Database()
    db.construct()

    # Create a sample portfolio
    obj = PortfolioObject(123)
    # obj.add_token("leo", 3)
    # obj.add_token("shib", 3)
    # obj.update_ethics_score(0.6)
    # obj.update_risk_score(0.2)

    # Add or update the portfolio in the database
    existing_portfolio = db.add_portfolio(obj)
    

    db.close_connection()
    
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=3332)
