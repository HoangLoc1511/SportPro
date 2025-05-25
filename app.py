import os
import uuid
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_cors import CORS
from chatbot_logic import handle_intent

app = Flask(__name__)

# Cấu hình secret_key lấy từ biến môi trường, có giá trị mặc định nếu không set
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-default-secret-key')

# Cấu hình session lưu trên filesystem
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# CORS: chỉ cho phép domain cụ thể truy cập (thay domain này thành domain website của bạn)
CORS(app, origins=["https://taxinhanhchong.com"], supports_credentials=True)

@app.route('/')
def index():
    # Nếu chưa có user_id trong session thì tạo mới
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['current_intent'] = None
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip().lower()
    current_intent = session.get('current_intent', None)

    # Xử lý các intent menu chính
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

    # Xử lý các luồng intent con
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

    # Fallback: không hiểu câu hỏi
    reply = handle_intent("fallback", user_input)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
