import stripe
from flask import Flask, request, abort
from config import STRIPE_SECRET_KEY, WEBHOOK_URL

stripe.api_key = STRIPE_SECRET_KEY
app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "alive"}

@app.route("/webhook", methods=["POST"])
def webhook():
    return {"status": "ok"}  # Simplified for now

@app.route("/success", methods=["GET"])
def success():
    return "Payment successful!"

@app.route("/cancel", methods=["GET"])
def cancel():
    return "Payment cancelled."
