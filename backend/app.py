from flask import Flask
from database import connect_w_db # From a python file in same dir

app = Flask(__name__)

@app.route("/")
def home():
    return "Drone Delivery Backend is running"

@app.route("/test")
def test():
    return "Test route is working!"

@app.route("/test-db")
def test_db():
    db = connect_w_db()
    if db.is_connected():
        db.close()
        return "Database connection successful"
    return "Database connection failed"

if __name__=="__main__":
    app.run(debug=True)