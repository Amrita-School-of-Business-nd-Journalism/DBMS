import os
import mysql.connector 
from dotenv import load_dotenv

load_dotenv()

def connect_w_db():
    db = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASSWORD", "180589"),
        database=os.environ.get("DB_NAME", "DRONEDELIVERY")
    )
    return db