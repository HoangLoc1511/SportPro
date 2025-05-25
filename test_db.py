import mysql.connector

try:
    conn = mysql.connector.connect(
        host='118.68.201.19',
        user='sa',
        password='123456',
        database='sportpro',
        port=3306
    )
    print("✅ Kết nối MySQL thành công!")
except Exception as e:
    print(f"❌ Lỗi: {e}")
