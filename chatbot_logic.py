from db import get_connection
import re

def handle_intent(intent, user_input):
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
        return "📦 Bạn muốn tư vấn sản phẩm nào? (ví dụ: giày, quần áo, dụng cụ thể thao, Nike, Adidas...)"

    elif intent == "product_advice_details":
        keyword = user_input.lower()
        if "nike" in keyword:
            return "🔥 Bộ sưu tập Nike: https://sportpro.vn/collections/nike"
        elif "adidas" in keyword:
            return "🔥 Bộ sưu tập Adidas: https://sportpro.vn/collections/adidas"
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT product_name, price, image_url
                FROM products
                WHERE product_name LIKE ?
            """, ('%' + keyword + '%',))

            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()

            if results:
                return "\n".join([
                    f"✔ {row['product_name']} – {row['price']} VND\n{row['image_url']}" for row in results
                ])
            else:
                return "❌ Không tìm thấy sản phẩm phù hợp. Bạn có thể thử lại với tên khác?"

    elif intent == "order_check_start":
        return "📦 Vui lòng nhập mã đơn hàng của bạn (ví dụ: SP20230501):"

    elif intent == "order_check_details":
        order_id = user_input.strip()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.status, o.total_amount, c.full_name
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_id = ?
        """, (order_id,))

        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        conn.close()

        if row:
            result = dict(zip(columns, row))
            return (
                f"📋 Mã đơn: {result['order_id']}\n"
                f"👤 Khách: {result['full_name']}\n"
                f"🧾 Trạng thái: {result['status']}\n"
                f"💰 Tổng tiền: {result['total_amount']} VND"
            )
        else:
            return "❌ Mã đơn không hợp lệ hoặc không tồn tại. Vui lòng kiểm tra lại."

    elif intent == "store_locator":
        keyword = user_input.lower()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT store_name, address, phone
            FROM stores
            WHERE city LIKE ?
        """, ('%' + keyword + '%',))

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        if results:
            return "\n\n".join([
                f"🏬 {row['store_name']}\n📍 {row['address']}\n📞 {row['phone']}" for row in results
            ])
        return "❌ Mình không tìm thấy cửa hàng nào ở khu vực bạn cung cấp. Bạn thử tên khác nhé!"

    elif intent == "faq":
        keyword = user_input.lower()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, answer FROM faqs WHERE topic LIKE ?
        """, ('%' + keyword + '%',))

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

        if results:
            return "\n\n".join([
                f"❓ {row['question']}\n💡 {row['answer']}" for row in results
            ])
        return "❌ Mình chưa có thông tin về chính sách đó. Bạn có thể hỏi: vận chuyển, đổi trả, bảo hành..."

    else:
        return (
            "🤖 Mình chưa hiểu câu hỏi của bạn.\n"
            "Bạn vui lòng chọn từ menu chính bằng cách nhắn 'menu'."
        )
