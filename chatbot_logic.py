from db import get_connection
import re

def handle_intent(intent, user_input):
    if intent == "welcome":
        return (
            "\U0001F389 Xin chào! Mình là trợ lý SportPro.\n"
            "Bạn muốn:\n"
            "1. Tư vấn sản phẩm\n"
            "2. Tra cứu đơn hàng\n"
            "3. Tìm cửa hàng\n"
            "4. Chính sách mua hàng"
        )

    # ---------- 1. TƯ VẤN SẢN PHẨM ----------
    elif intent == "product_advice":
        return (
            "\U0001F4E6 Bạn muốn tư vấn sản phẩm nào?\n"
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
                return f"\U0001F525 Bộ sưu tập {brand.capitalize()}: {brand_links[brand]}"

        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT product_name, price, color, size, image_url
                        FROM products
                        WHERE product_name LIKE ? OR color LIKE ? OR size LIKE ?
                    """, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
                    columns = [column[0] for column in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            # Log error nếu có hệ thống logging (đề xuất)
            # logger.error(f"Lỗi truy vấn sản phẩm: {e}")
            return f"⚠️ Lỗi hệ thống khi tìm sản phẩm. Vui lòng thử lại sau."

        if results:
            return "\n\n".join([
                f"\u2714 {row['product_name']}\nMàu: {row['color']} | Size: {row['size']}\nGiá: {row['price']} VND\nẢnh: {row['image_url']}"
                for row in results
            ])
        else:
            return (
                "\u274C Không tìm thấy sản phẩm phù hợp với từ khóa bạn nhập.\n"
                "Bạn có thể thử lại với tên sản phẩm hoặc thương hiệu khác như: 'áo thể thao', 'giày nike', 'túi adidas'..."
            )

    # ---------- 2. TRA CỨU ĐƠN HÀNG ----------
    elif intent == "order_check_start":
        return "\U0001F4E6 Vui lòng nhập mã đơn hàng của bạn (ví dụ: SP20230501):"

    elif intent == "order_check_details":
        order_id = user_input.strip()
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT o.order_id, o.status, o.total_amount, o.order_date, c.full_name, o.delivery_address
                        FROM orders o
                        JOIN customers c ON o.customer_id = c.customer_id
                        WHERE o.order_id = ?
                    """, (order_id,))
                    columns = [column[0] for column in cursor.description]
                    row = cursor.fetchone()
        except Exception as e:
            return f"⚠️ Lỗi hệ thống khi tra cứu đơn hàng. Vui lòng thử lại sau."

        if row:
            result = dict(zip(columns, row))
            return (
                f"\U0001F4CB Mã đơn: {result['order_id']}\n"
                f"\U0001F464 Khách: {result['full_name']}\n"
                f"📅 Ngày đặt: {result['order_date']}\n"
                f"\U0001F9FE Trạng thái: {result['status']}\n"
                f"\U0001F4B0 Tổng tiền: {result['total_amount']} VND\n"
                f"\U0001F4CD Giao đến: {result['delivery_address']}"
            )
        else:
            return "\u274C Mã đơn không hợp lệ hoặc không tồn tại. Vui lòng kiểm tra lại."

    # ---------- 3. TÌM CỬA HÀNG ----------
    elif intent == "store_locator":
        keyword = user_input.lower()
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT store_name, address, phone, opening_hours
                        FROM stores
                        WHERE city LIKE ?
                    """, ('%' + keyword + '%',))
                    columns = [column[0] for column in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            return f"⚠️ Lỗi hệ thống khi tìm cửa hàng. Vui lòng thử lại sau."

        if results:
            return "\n\n".join([
                f"\U0001F3EC {row['store_name']}\n\U0001F4CD {row['address']}\n\U0001F4DE {row['phone']}\n🕒 Giờ mở cửa: {row['opening_hours']}"
                for row in results
            ])
        else:
            return "\u274C Mình không tìm thấy cửa hàng nào ở khu vực bạn cung cấp. Bạn thử tên khác nhé!"

    # ---------- 4. HỎI VỀ CHÍNH SÁCH ----------
    elif intent == "faq":
        keyword = user_input.lower()
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT question, answer FROM faqs WHERE topic LIKE ?
                    """, ('%' + keyword + '%',))
                    columns = [column[0] for column in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            return f"⚠️ Lỗi hệ thống khi tìm hiểu chính sách. Vui lòng thử lại sau."

        if results:
            return "\n\n".join([
                f"\u2753 {row['question']}\n\U0001F4A1 {row['answer']}" for row in results
            ])
        else:
            return "\u274C Mình chưa có thông tin về chính sách đó. Bạn có thể hỏi: vận chuyển, đổi trả, bảo hành..."

    # ---------- MẶC ĐỊNH ----------
    else:
        return (
            "\U0001F916 Mình chưa hiểu câu hỏi của bạn.\n"
            "Bạn vui lòng chọn từ menu chính bằng cách nhắn 'menu'."
        )
