import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
PRODUCT_PRICE_ID = os.getenv("PRODUCT_PRICE_ID", "price_123456789")  # Your Stripe price ID
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app.railway.app")  # Your Railway URL
