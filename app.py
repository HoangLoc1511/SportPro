from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_cors import CORS  # <-- import thư viện CORS
import uuid
from chatbot_logic import handle_intent
from db import get_connection

app = Flask(__name__)
CORS(app, origins=["https://taxinhanhchong.com/"])  # <-- thêm dòng này để cho phép CORS với domain WordPress

app.secret_key = 'secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Trang chính: chatbot UI
@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['current_intent'] = None
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip().lower()
    current_intent = session.get('current_intent', None)

    # Người dùng gọi menu hoặc chào hỏi
    if user_input in ['hi', 'hello', 'xin chào', 'chào', 'menu']:
        session['current_intent'] = "welcome"
        return jsonify({"reply": handle_intent("welcome", user_input)})

    # Người dùng chọn 1 - tư vấn sản phẩm
    if user_input in ['1', 'tư vấn', 'tư vấn sản phẩm']:
        session['current_intent'] = "product_advice"
        return jsonify({"reply": handle_intent("product_advice", user_input)})

    # Người dùng chọn 2 - tra cứu đơn hàng
    if user_input in ['2', 'tra cứu', 'tra đơn', 'đơn hàng']:
        session['current_intent'] = "order_check_start"
        return jsonify({"reply": handle_intent("order_check_start", user_input)})

    # Người dùng chọn 3 - tìm cửa hàng
    if user_input in ['3', 'tìm cửa hàng', 'cửa hàng']:
        session['current_intent'] = "store_locator"
        return jsonify({"reply": handle_intent("store_locator", user_input)})

    # Người dùng chọn 4 - hỏi chính sách
    if user_input in ['4', 'chính sách', 'faq']:
        session['current_intent'] = "faq"
        return jsonify({"reply": handle_intent("faq", user_input)})

    # Xử lý luồng chi tiết dựa trên intent hiện tại

    # Luồng tư vấn sản phẩm
    if current_intent == "product_advice":
        session['current_intent'] = "product_advice_details"
        return jsonify({"reply": handle_intent("product_advice_details", user_input)})

    if current_intent == "product_advice_details":
        session['current_intent'] = None
        return jsonify({"reply": handle_intent("product_advice_details", user_input)})

    # Luồng tra cứu đơn hàng
    if current_intent == "order_check_start":
        session['current_intent'] = "order_check_details"
        return jsonify({"reply": handle_intent("order_check_details", user_input)})

    if current_intent == "order_check_details":
        session['current_intent'] = None
        return jsonify({"reply": handle_intent("order_check_details", user_input)})

    # Luồng tìm cửa hàng
    if current_intent == "store_locator":
        session['current_intent'] = None
        return jsonify({"reply": handle_intent("store_locator", user_input)})

    # Luồng hỏi chính sách
    if current_intent == "faq":
        session['current_intent'] = None
        return jsonify({"reply": handle_intent("faq", user_input)})

    # Fallback khi không nhận dạng được intent
    return jsonify({"reply": handle_intent("fallback", user_input)})

if __name__ == '__main__':
    app.run(debug=True)