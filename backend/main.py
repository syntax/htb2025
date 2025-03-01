from app import app
import database

if __name__ == '__main__':
    db = database.Database()
    db.construct()
    db.close_connection()
    app.run(debug=True, host='0.0.0.0', port=3333)
