from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_cors import CORS
import uuid
from chatbot_logic import handle_intent

app = Flask(__name__)

# CORS: thay bằng domain WordPress của bạn
CORS(app, origins=["https://taxinhanhchong.com"], supports_credentials=True)

app.secret_key = 'your-secret-key'  # Đổi thành chuỗi bí mật của bạn
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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

if __name__ == '__main__':
    # Port Render.com thường cung cấp qua biến môi trường PORT
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
