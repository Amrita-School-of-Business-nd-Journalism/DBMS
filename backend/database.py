import mysql.connector 

def connect_w_db():
    db = mysql.connector.connect(
        host="localhost",
        user="admin", # beware
        password="180589", # beware
        database="DRONEDELIVERY"
    )
    return db