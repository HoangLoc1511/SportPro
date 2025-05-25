import pyodbc

def get_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ADMIN-PC;'  # hoặc 'Tên_Máy_Tính' nếu từ máy khác
        'DATABASE=sportpro;'  # thay bằng tên database của bạn
        'Trusted_Connection=yes;'
    )
    return conn

try:
    conn = get_connection()
    print("✅ Kết nối thành công!")
    conn.close()
except Exception as e:
    print("❌ Kết nối thất bại:", e)
