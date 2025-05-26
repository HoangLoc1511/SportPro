import os
import uuid
import logging
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
from flask_cors import CORS
from chatbot_logic import handle_intent  # Import chatbot logic
from db import get_connection  # Import database connection

# Configure logging to track errors and info
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Initialize the Flask application
app = Flask(__name__)

# CORS: Allow specific domains for security (you can replace with your domain)
CORS(app, origins=["https://taxinhanhchong.com"], supports_credentials=True)

# Configure session to keep track of user data
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')  # Replace with your secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    # Create a new user_id if not in the session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['current_intent'] = None
    return render_template('index.html')

@app.route('/test_db')
def test_db():
    try:
        # Test DB connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple query to test connection
        cursor.close()
        conn.close()
        logging.info("Database connection successful.")
        return "✅ Database connection successful!"
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return f"❌ Database connection failed: {e}"

@app.route('/query', methods=['GET'])
def query_db():
    try:
        # Fetch products from the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, price FROM products")  # Query to fetch products
        rows = cursor.fetchall()

        # Prepare results as a list of dictionaries
        results = [{'product_name': row[0], 'price': row[1]} for row in rows]
        cursor.close()
        conn.close()
        return jsonify(results)  # Return the results as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message", "").strip().lower()
        current_intent = session.get('current_intent', None)

        # Process different intents based on user input
        if user_input in ['hi', 'hello', 'xin chào', 'chào', 'menu']:
            session['current_intent'] = "welcome"
            reply = handle_intent("welcome", user_input)
            return jsonify({"reply": reply})

        # Process other intents like product advice, order check, etc.
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

        # Handle nested intents like product advice details
        if current_intent == "product_advice":
            session['current_intent'] = "product_advice_details"
            reply = handle_intent("product_advice_details", user_input)
            return jsonify({"reply": reply})

        if current_intent == "product_advice_details":
            session['current_intent'] = None
            reply = handle_intent("product_advice_details", user_input)
            return jsonify({"reply": reply})

        # Fallback for unknown inputs
        reply = handle_intent("fallback", user_input)
        return jsonify({"reply": reply})

    except Exception as e:
        logging.error(f"Error processing chat request: {e}")
        return jsonify({"reply": "❌ Error occurred, please try again later."})

# Start Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Port provided by Render or environment variable
    app.run(debug=True, host='0.0.0.0', port=port)
