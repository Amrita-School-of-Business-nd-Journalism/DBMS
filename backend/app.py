from flask import Flask, jsonify, request
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

@app.route("/users")
def users():
    db = connect_w_db()
    cursor = db.cursor()
    cursor.execute("select * from USERS")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

@app.route("/test-post",methods=["POST"])
def test_post():
    data = request.get_json()
    return jsonify({
        "message":"Post Successful",
        "rec_data":data
    })

@app.route("/login",methods=["POST"])
def login():
    
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    role = data["role"]
    
    db = connect_w_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT USER_ID, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD_HASH, ROLE
    FROM USERS
    WHERE EMAIL=%s AND ROLE=%s
    """

    cursor.execute(query,(email,role))
    user = cursor.fetchone()
    
    cursor.close()
    db.close()

    return jsonify({
        "email":email,
        "password":password,
        "role":role
    })

if __name__=="__main__":
    app.run(debug=True)