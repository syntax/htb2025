from app import app
from database import Database
from app import PortfolioObject

if __name__ == "__main__":
    db = Database()
    db.construct()

    # Create a sample portfolio
    obj = PortfolioObject(123)

    # Add or update the portfolio in the database
    existing_portfolio = db.add_portfolio(obj)
    

    db.close_connection()
    
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=3332)
