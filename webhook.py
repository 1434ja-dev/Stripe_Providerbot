from flask import Flask, request, jsonify
import config
import stripe

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "bot_token": "✅" if config.BOT_TOKEN else "❌",
        "stripe_key": "✅" if config.STRIPE_SECRET_KEY else "❌"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    """Stripe webhook endpoint"""
    return jsonify({"status": "received"}), 200

@app.route("/success", methods=["GET"])
def success():
    return "✅ Payment successful!"

@app.route("/cancel", methods=["GET"])
def cancel():
    return "❌ Payment cancelled."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT)
