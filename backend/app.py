from flask import Flask, jsonify, request, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import connect_w_db # From a python file in dir ../database
from mysql.connector import IntegrityError
# from flask_cors import CORS - Removed after joining webpages in the routing

app = Flask(__name__)
app.secret_key = "DBMS-DroneApp"

# Home Page - Login Page Render
@app.route("/")
def home():
    return render_template("index.html")

# Welcome Customer - Customer Page Render with Session
@app.route("/customer")
def customer_dashboard():
    if "USER_ID" not in session:
        return "Please login first", 401
    if session["ROLE"] != "CUSTOMER":
        return "Access denied", 403
    return render_template("customer.html")

# Welcome Vendor - Vendor Page Render with Session
@app.route("/vendor")
def vendor_dashboard():
    if "USER_ID" not in session:
        return "Please login first", 401
    if session["ROLE"] != "VENDOR":
        return "Access denied", 403
    return render_template("vendor.html")

# Logging out - Session Clear
@app.route("/logout")
def logout():
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })

# Registering a new account - Register Page Render with Session
@app.route("/register")
def register_page():
    return render_template("register.html")

# Register Flask Backend + MariaDB - CREATE (INSERT)
@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    phone_no = data["phone_no"]
    password = data["password"]
    role = data["role"]

    password_hash = generate_password_hash(password)

    db = connect_w_db()
    cursor = db.cursor()

    query = """
        INSERT INTO USERS(FIRST_NAME,LAST_NAME,EMAIL,
        PHONE_NO,PASSWORD_HASH,CREATED_AT,ROLE)
        VALUES(%s,%s,%s,%s,%s,CURDATE(),%s)
    """

    try:
        cursor.execute(query, (
            first_name,
            last_name,
            email,
            phone_no,
            password_hash,
            role
        ))

        db.commit()

    except IntegrityError:
        db.rollback()

        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 409

    finally:
        cursor.close()
        db.close()
    
    return jsonify({
        "success": True,
        "message": "Registration successful"
    })

# Users Table GET request
@app.route("/users")
def users():
    db = connect_w_db()
    cursor = db.cursor()
    cursor.execute("select USER_ID,FIRST_NAME,LAST_NAME,EMAIL,ROLE from USERS")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(users)

# Login Flask Backend + MariaDB - READ (SELECT WHERE)
@app.route("/login",methods=["POST"])
def login_user():
    
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


    if user is None:
        return jsonify({
            "success":False,
            "message":"User not found!"
        }), 401

    is_password_correct = check_password_hash(user["PASSWORD_HASH"],password)
    
    if not is_password_correct:
        return jsonify({
            "success": False,
            "message": "Invalid password"
        }), 401
    session["USER_ID"] = user["USER_ID"]
    session["ROLE"] = user["ROLE"]
 
    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "USER_ID": user["USER_ID"],
            "FIRST_NAME": user["FIRST_NAME"],
            "LAST_NAME": user["LAST_NAME"],
            "EMAIL": user["EMAIL"],
            "ROLE": user["ROLE"]
        }
    })

# Profile - User Fetching Route (Displaying in customer.html)
@app.route("/profile")
def get_profile():
    
    if "USER_ID" not in session:
        return jsonify({
            "success" : False,
            "message" : "Please login first"
        }), 401
    
    db = connect_w_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT USER_ID, FIRST_NAME, LAST_NAME,
        EMAIL, PHONE_NO, ROLE
        FROM USERS WHERE USER_ID = %s
    """,(session["USER_ID"],))

    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user is None:
        return jsonify({
            "success":False,
            "message":"User not found"
        }), 404
    
    return jsonify({
        "success":True,
        "user":user
    })

# Profile - User Submitting Reflecting in DB
@app.route("/profile", methods=["PUT"])
def update_profile():
    if "USER_ID" not in session:
        return jsonify({
            "success" : False,
            "message" : "Please login first"
        }), 401
    
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone_no = data["phone_no"]

    db = connect_w_db()
    cursor = db.cursor()

    query = """
        UPDATE USERS 
        SET FIRST_NAME = %s,
        LAST_NAME = %s,
        PHONE_NO = %s 
        WHERE USER_ID = %s
    """

    cursor.execute(query,(first_name,last_name,phone_no,session["USER_ID"]))
    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "success":True,
        "message":"User Details updated Successfully"
    })

# Profile - User Delete Track
@app.route("/profile", methods=["DELETE"])
def delete_profile():
    if "USER_ID" not in session:
        return jsonify({
            "success":False,
            "message":"Please Login First"
        }),401
    db = connect_w_db()
    cursor = db.cursor()

    query = """
    DELETE FROM USERS WHERE USER_ID = %s
    """
    cursor.execute(query,(session["USER_ID"],))

    db.commit()
    cursor.close()
    db.close()
    session.clear()

    return jsonify({
        "success":True,
        "message":"Account Deleted Successfully"
    })

# Running the App
if __name__=="__main__":
    app.run(debug=True)