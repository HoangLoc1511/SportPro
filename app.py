import os
import uuid
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_cors import CORS
from chatbot_logic import handle_intent

app = Flask(__name__)

# Cấu hình CORS: thay bằng domain website bạn cho phép (vd: WordPress)
CORS(app, origins=["https://taxinhanhchong.com"], supports_credentials=True)

# Lấy secret key từ biến môi trường
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# Cấu hình session lưu file hệ thống
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    # Tạo user_id session nếu chưa có
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['current_intent'] = None
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip().lower()
    current_intent = session.get('current_intent', None)
@app.route('/test_db')
def test_db():
    try:
        conn = get_connection()  # Gọi hàm get_connection của bạn
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Thực hiện truy vấn cơ bản để kiểm tra kết nối
        return "Kết nối cơ sở dữ liệu thành công!"
    except Exception as e:
        return f"Kết nối thất bại: {e}"

    # Xử lý menu chính & intent chính
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

    # Xử lý các intent theo luồng
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

    # Fallback nếu không hiểu input
    reply = handle_intent("fallback", user_input)
    return jsonify({"reply": reply})

# Route test biến môi trường (xóa hoặc comment sau khi test xong)
@app.route('/env')
def env():
    return {
        "DB_SERVER": os.getenv('DB_SERVER'),
        "DB_NAME": os.getenv('DB_NAME'),
        "DB_USER": os.getenv('DB_USER'),
        "FLASK_SECRET_KEY": os.getenv('FLASK_SECRET_KEY'),
        "PORT": os.getenv('PORT')
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', '10000'))
    app.run(host='0.0.0.0', port=port)
