import stripe
from config import STRIPE_SECRET_KEY, PRODUCT_PRICE_ID, WEBHOOK_URL

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(price_id: str, user_id: int) -> str:
    """Create a Stripe Checkout session and return the URL"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",  # or "payment" for one-time
            success_url=f"{WEBHOOK_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{WEBHOOK_URL}/cancel",
            metadata={
                "telegram_user_id": str(user_id)
            }
        )
        return session.url
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None

# Flask webhook handler (for Railway deployment)
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        abort(400)
    except stripe.error.SignatureVerificationError:
        abort(400)

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("telegram_user_id")
        print(f"Payment successful for user {user_id}")
        # Here you would grant access to the user in your database

    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
