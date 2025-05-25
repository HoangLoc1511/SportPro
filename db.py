import os
import pyodbc

def get_connection():
    # Lấy biến môi trường để cấu hình kết nối
    server = os.getenv('DB_SERVER', 'ADMIN-PC')
    database = os.getenv('DB_NAME', 'sportpro')
    username = os.getenv('DB_USER', 'Admin')
    password = os.getenv('DB_PASS', '123456')
    driver = '{ODBC Driver 17 for SQL Server}'

    if username and password:
        # Kết nối dùng SQL Server Authentication
        conn_str = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
    else:
        # Kết nối dùng Windows Authentication (chỉ dùng được trên Windows)
        conn_str = (
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )

    return pyodbc.connect(conn_str)
