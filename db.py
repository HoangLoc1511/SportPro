import os
import pyodbc

def get_connection():
    server = os.getenv('DB_SERVER', 'ADMIN-PC')   # Tên máy chủ SQL Server hoặc IP
    database = os.getenv('DB_NAME', 'sportpro')   # Tên database
    username = os.getenv('DB_USER', 'Admin') 
    driver = '{ODBC Driver 17 for SQL Server}'

    conn_str = (
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'UID={username};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )

    try:
        connection = pyodbc.connect(conn_str)
        return connection
    except pyodbc.Error as e:
        print(f"Lỗi kết nối CSDL: {e}")
        raise
