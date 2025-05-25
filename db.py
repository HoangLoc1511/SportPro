import os
import mysql.connector
from mysql.connector import Error

def get_connection():
    server = os.getenv('DB_SERVER', '118.68.201.19')  # Public IP của bạn
    database = os.getenv('DB_NAME', 'sportpro')
    username = os.getenv('DB_USER', 'sa')
    password = os.getenv('DB_PASSWORD', '123456')
    driver = '{ODBC Driver 17 for SQL Server}'

    conn_str = (
        f'DRIVER={driver};'
        f'SERVER={server},1433;'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )

    try:
        connection = pyodbc.connect(conn_str)
        return connection
    except pyodbc.Error as e:
        print(f"Lỗi kết nối CSDL: {e}")
        raise

