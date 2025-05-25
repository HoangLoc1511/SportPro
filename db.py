import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ADMIN-PC;'  # hoặc 'Tên_Máy_Tính' nếu từ máy khác
        'DATABASE=sportpro;'  # thay bằng tên database của bạn
        'Trusted_Connection=yes;'
    )
    return conn