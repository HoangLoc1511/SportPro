import os
import pyodbc
from dotenv import load_dotenv

# Tự động tải các biến môi trường từ file .env (chỉ dùng khi chạy local)
load_dotenv()

def get_connection():
    server = os.getenv('DB_SERVER', '127.0.0.1')   # IP public hoặc 'localhost'
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
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"❌ Lỗi kết nối CSDL: {e}")
        raise
