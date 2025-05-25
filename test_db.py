from db import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")  # Truy vấn đơn giản để test
    print("✅ Kết nối cơ sở dữ liệu thành công!")
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
