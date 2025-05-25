import os
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_SERVER', 'ADMIN-PC'),  # hoặc IP Public
            port=int(os.getenv('DB_PORT', 3306, 10000)),
            database=os.getenv('DB_NAME', 'sportpro'),
            user=os.getenv('DB_USER', 'sa'),
            password=os.getenv('DB_PASSWORD', '123456')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
        raise
