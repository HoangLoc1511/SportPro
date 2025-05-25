import logging
from db import get_connection

logging.basicConfig(level=logging.INFO)

def handle_intent(intent, user_input):
    try:
        if intent == "welcome":
            return (
                "🎉 Xin chào! Mình là trợ lý SportPro.\n"
                "Bạn muốn:\n"
                "1. Tư vấn sản phẩm\n"
                "2. Tra cứu đơn hàng\n"
                "3. Tìm cửa hàng\n"
                "4. Chính sách mua hàng"
            )

        elif intent == "product_advice":
            return (
                "📦 Bạn muốn tư vấn sản phẩm nào?\n"
                "Hãy nhập tên sản phẩm (giày, quần áo...) hoặc thương hiệu (Nike, Adidas)."
            )

        elif intent == "product_advice_details":
            conn = get_connection()
            cursor = conn.cursor()
            keyword = f"%{user_input}%"
            cursor.execute("""
                SELECT TOP 3 product_name, price, color, size, image_url
                FROM products
                WHERE product_name LIKE ? OR color LIKE ? OR size LIKE ?
            """, (keyword, keyword, keyword))

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if rows:
                return "\n\n".join([
                    f"✔ {r[0]}\nMàu: {r[2]} | Size: {r[3]}\nGiá: {r[1]} VND\nẢnh: {r[4]}"
                    for r in rows
                ])
            else:
                return "❌ Không tìm thấy sản phẩm phù hợp. Vui lòng thử lại."

        elif intent == "order_check_start":
            return "📦 Vui lòng nhập mã đơn hàng của bạn (ví dụ: SP20230501):"

        elif intent == "order_check_details":
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_id, c.full_name, o.order_date, o.status, o.total_amount, o.delivery_address
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.order_id = ?
            """, (user_input.strip(),))

            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                return (
                    f"📋 Đơn hàng: {row[0]}\n"
                    f"👤 Khách: {row[1]}\n"
                    f"📅 Ngày: {row[2]}\n"
                    f"🧾 Trạng thái: {row[3]}\n"
                    f"💰 Tổng: {row[4]} VND\n"
                    f"📍 Giao đến: {row[5]}"
                )
            else:
                return "❌ Mã đơn không tồn tại. Vui lòng kiểm tra lại."

        elif intent == "store_locator":
            conn = get_connection()
            cursor = conn.cursor()
            keyword = f"%{user_input}%"
            cursor.execute("""
                SELECT store_name, address, phone, opening_hours
                FROM stores
                WHERE city LIKE ?
            """, (keyword,))
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            if results:
                return "\n\n".join([
                    f"🏬 {r[0]}\n📍 {r[1]}\n📞 {r[2]}\n🕒 Giờ mở: {r[3]}"
                    for r in results
                ])
            else:
                return "❌ Không tìm thấy cửa hàng ở khu vực bạn cung cấp."

        elif intent == "faq":
            conn = get_connection()
            cursor = conn.cursor()
            keyword = f"%{user_input}%"
            cursor.execute("""
                SELECT question, answer FROM faqs WHERE topic LIKE ?
            """, (keyword,))
            faqs = cursor.fetchall()
            cursor.close()
            conn.close()

            if faqs:
                return "\n\n".join([
                    f"❓ {q}\n💡 {a}" for q, a in faqs
                ])
            else:
                return "❌ Không có chính sách nào phù hợp với câu hỏi của bạn."

        else:
            return "🤖 Mình chưa hiểu. Bạn có thể nhắn 'menu' để xem các tùy chọn."

    except Exception as e:
        logging.error(f"Lỗi xử lý intent {intent}: {e}")
        return "⚠️ Đã có lỗi hệ thống, vui lòng thử lại sau."
