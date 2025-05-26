import os
import uuid
import logging
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_cors import CORS
from chatbot_logic import handle_intent
from db import get_connection

# Cấu hình logging để theo dõi lỗi và thông tin
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

# CORS: Chỉ cho phép một số domain nhất định để bảo mật
CORS(app, origins=["https://taxinhanhchong.com"], supports_credentials=True)

# Cấu hình session
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'a8f5f167f44f4964e6c998dee827110c')  # Đổi thành chuỗi bí mật của bạn
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    # Tạo user_id mới nếu chưa có session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['current_intent'] = None
    return render_template('index.html')

@app.route('/test_db')
def test_db():
    try:
        # Kiểm tra kết nối cơ sở dữ liệu
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Truy vấn đơn giản để kiểm tra kết nối
        cursor.close()
        conn.close()
        logging.info("Kết nối cơ sở dữ liệu thành công.")
        return "✅ Kết nối cơ sở dữ liệu thành công!"
    except Exception as e:
        logging.error(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return f"❌ Kết nối thất bại: {e}"
# Route để truy vấn và trả kết quả ra HTML
@app.route('/query', methods=['GET'])
def query_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, price FROM products")  # Truy vấn cơ sở dữ liệu
        rows = cursor.fetchall()  # Lấy tất cả kết quả truy vấn

        # Chuyển kết quả truy vấn thành dạng danh sách
        results = [{'product_name': row[0], 'price': row[1]} for row in rows]
        cursor.close()
        conn.close()

        return jsonify(results)  # Trả lại kết quả dưới dạng JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message", "").strip().lower()
        current_intent = session.get('current_intent', None)

        # Menu & intent chính
        if user_input in ['hi', 'hello', 'xin chào', 'chào', 'menu']:
            session['current_intent'] = "welcome"
            reply = handle_intent("welcome", user_input)
            return jsonify({"reply": reply})

        if user_input in ['1', 'tư vấn', 'tư vấn sản phẩm']:
            session['current_intent'] = "product_advice"
            reply = handle_intent("product_advice", user_input)
            return jsonify({"reply": reply})

        if user_input in ['2', 'tra cứu', 'tra đơn', 'đơn hàng']:
            session['current_intent'] = "order_check_start"
            reply = handle_intent("order_check_start", user_input)
            return jsonify({"reply": reply})

        if user_input in ['3', 'tìm cửa hàng', 'cửa hàng']:
            session['current_intent'] = "store_locator"
            reply = handle_intent("store_locator", user_input)
            return jsonify({"reply": reply})

        if user_input in ['4', 'chính sách', 'faq']:
            session['current_intent'] = "faq"
            reply = handle_intent("faq", user_input)
            return jsonify({"reply": reply})

        # Xử lý theo luồng intent
        if current_intent == "product_advice":
            session['current_intent'] = "product_advice_details"
            reply = handle_intent("product_advice_details", user_input)
            return jsonify({"reply": reply})

        if current_intent == "product_advice_details":
            session['current_intent'] = None
            reply = handle_intent("product_advice_details", user_input)
            return jsonify({"reply": reply})

        if current_intent == "order_check_start":
            session['current_intent'] = "order_check_details"
            reply = handle_intent("order_check_details", user_input)
            return jsonify({"reply": reply})

        if current_intent == "order_check_details":
            session['current_intent'] = None
            reply = handle_intent("order_check_details", user_input)
            return jsonify({"reply": reply})

        if current_intent == "store_locator":
            session['current_intent'] = None
            reply = handle_intent("store_locator", user_input)
            return jsonify({"reply": reply})

        if current_intent == "faq":
            session['current_intent'] = None
            reply = handle_intent("faq", user_input)
            return jsonify({"reply": reply})

        # Fallback
        reply = handle_intent("fallback", user_input)
        return jsonify({"reply": reply})

    except Exception as e:
        # Log lỗi
        logging.error(f"Lỗi xử lý yêu cầu chat: {e}")
        return jsonify({"reply": "❌ Đã xảy ra lỗi, vui lòng thử lại sau."})

def handle_intent(intent, user_input):
    """
    Xử lý các intent của chatbot, bao gồm tư vấn sản phẩm, tra cứu đơn hàng, tìm cửa hàng, và chính sách.
    """
    if intent == "welcome":
        return "Chào bạn! Bạn muốn làm gì hôm nay? (Chọn 1, 2, 3, 4)"

    elif intent == "product_advice":
        return "Bạn muốn tư vấn sản phẩm nào? Ví dụ: giày, quần áo, dụng cụ thể thao..."

    elif intent == "product_advice_details":
        # Xử lý theo loại sản phẩm, ví dụ: giày, quần áo, hoặc các thương hiệu
        if 'giày' in user_input:
            return "Chúng tôi có các mẫu giày Nike, Adidas. Bạn muốn chọn mẫu nào?"
        elif 'quần áo' in user_input:
            return "Bạn muốn chọn quần áo thể thao nào? Chúng tôi có nhiều mẫu của Adidas và Nike."
        else:
            return "Chúng tôi không hiểu yêu cầu của bạn. Hãy thử lại."

    elif intent == "order_check_start":
        return "Vui lòng nhập mã đơn hàng của bạn."

    elif intent == "order_check_details":
        # Giả sử ta tra cứu thông tin đơn hàng từ CSDL
        return check_order_status(user_input)

    elif intent == "store_locator":
        return "Bạn muốn tìm cửa hàng ở đâu?"

    elif intent == "faq":
        return "Bạn muốn hỏi về chính sách nào? (Vận chuyển, đổi trả, bảo hành)"

    elif intent == "fallback":
        return "Xin lỗi, tôi không hiểu yêu cầu của bạn. Vui lòng thử lại."

    return "Tôi không hiểu yêu cầu của bạn. Vui lòng thử lại."

def check_order_status(order_id):
    """
    Kiểm tra trạng thái đơn hàng từ cơ sở dữ liệu.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        if order:
            return f"Đơn hàng {order[0]} hiện tại có trạng thái {order[3]}."
        else:
            return "Không tìm thấy đơn hàng với mã này."
    except Exception as e:
        logging.error(f"Lỗi tra cứu đơn hàng: {e}")
        return "Đã xảy ra lỗi khi tra cứu đơn hàng."

if __name__ == '__main__':
    # Port Render.com thường cung cấp qua biến môi trường PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
