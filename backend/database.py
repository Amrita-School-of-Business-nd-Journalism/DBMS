import mysql.connector 

def connect_w_db():
    db = mysql.connector.connect(
        host="localhost",
        user="bhuvan1707", # beware
        password="180589",
        database="DRONEDELIVERY"
    )
    return db