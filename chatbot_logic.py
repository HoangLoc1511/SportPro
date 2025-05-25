import logging
from db import get_connection

# Cấu hình logging để dễ dàng theo dõi lỗi và thông tin
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def handle_intent(intent, user_input):
    logging.info(f"Xử lý intent: {intent}, input: {user_input}")

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

        # 1. Tư vấn sản phẩm
        elif intent == "product_advice":
            return (
                "📦 Bạn muốn tư vấn sản phẩm nào?\n"
                "Bạn có thể nhập tên sản phẩm (ví dụ: giày, quần áo, túi),\n"
                "hoặc tên thương hiệu như Nike, Adidas để được gợi ý."
            )

        elif intent == "product_advice_details":
            keyword = user_input.lower()
            brand_links = {
                "nike": "https://sportpro.vn/collections/nike",
                "adidas": "https://sportpro.vn/collections/adidas",
                "converse": "https://sportpro.vn/collections/converse"
            }

            for brand in brand_links:
                if brand in keyword:
                    return f"🔥 Bộ sưu tập {brand.capitalize()}: {brand_links[brand]}"

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT product_name, price, color, size, image_url
                FROM products
                WHERE product_name LIKE ? OR color LIKE ? OR size LIKE ?
            """, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            if results:
                return "\n\n".join([
                    f"✔ {row['product_name']}\nMàu: {row['color']} | Size: {row['size']}\nGiá: {row['price']} VND\nẢnh: {row['image_url']}"
                    for row in results
                ])
            else:
                return (
                    "❌ Không tìm thấy sản phẩm phù hợp với từ khóa bạn nhập.\n"
                    "Bạn có thể thử lại với tên sản phẩm hoặc thương hiệu khác như: 'áo thể thao', 'giày nike', 'túi adidas'..."
                )

        # 2. Tra cứu đơn hàng
        elif intent == "order_check_start":
            return "📦 Vui lòng nhập mã đơn hàng của bạn (ví dụ: SP20230501):"

        elif intent == "order_check_details":
            order_id = user_input.strip()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT o.order_id, o.status, o.total_amount, o.order_date, c.full_name, o.delivery_address
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.order_id = ?
            """, (order_id,))

            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                columns = [desc[0] for desc in cursor.description]
                result = dict(zip(columns, row))
                return (
                    f"📋 Mã đơn: {result['order_id']}\n"
                    f"👤 Khách: {result['full_name']}\n"
                    f"📅 Ngày đặt: {result['order_date']}\n"
                    f"🧾 Trạng thái: {result['status']}\n"
                    f"💰 Tổng tiền: {result['total_amount']} VND\n"
                    f"📍 Giao đến: {result['delivery_address']}"
                )
            else:
                return "❌ Mã đơn không hợp lệ hoặc không tồn tại. Vui lòng kiểm tra lại."

        # 3. Tìm cửa hàng
        elif intent == "store_locator":
            keyword = user_input.lower()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT store_name, address, phone, opening_hours
                FROM stores
                WHERE city LIKE ?
            """, ('%' + keyword + '%',))

            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            if results:
                return "\n\n".join([
                    f"🏬 {row['store_name']}\n📍 {row['address']}\n📞 {row['phone']}\n🕒 Giờ mở cửa: {row['opening_hours']}"
                    for row in results
                ])
            else:
                return "❌ Mình không tìm thấy cửa hàng nào ở khu vực bạn cung cấp. Bạn thử tên khác nhé!"

        # 4. Hỏi về chính sách
        elif intent == "faq":
            keyword = user_input.lower()
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT question, answer FROM faqs WHERE topic LIKE ?
            """, ('%' + keyword + '%',))

            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            if results:
                return "\n\n".join([
                    f"❓ {row['question']}\n💡 {row['answer']}"
                    for row in results
                ])
            else:
                return "❌ Mình chưa có thông tin về chính sách đó. Bạn có thể hỏi: vận chuyển, đổi trả, bảo hành..."

        # Fallback cho các câu không nhận dạng được intent
        else:
            return (
                "🤖 Mình chưa hiểu câu hỏi của bạn.\n"
                "Bạn vui lòng chọn từ menu chính bằng cách nhắn 'menu'."
            )

    except Exception as e:
        logging.error(f"Lỗi xử lý intent '{intent}': {e}")
        return "⚠️ Đã xảy ra lỗi hệ thống, vui lòng thử lại sau."