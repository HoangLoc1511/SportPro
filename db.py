import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()  # load biến môi trường từ file .env

def get_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
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
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        print(f"❌ Lỗi kết nối CSDL: {e}")
        raise
