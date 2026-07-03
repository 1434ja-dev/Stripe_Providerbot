import os
from dotenv import load_dotenv

load_dotenv()

# Required variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
PRODUCT_PRICE_ID = os.getenv("PRODUCT_PRICE_ID", "price_test")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app.railway.app")
PORT = int(os.getenv("PORT", 8080))

if not BOT_TOKEN:
    print("⚠️ WARNING: BOT_TOKEN not set!")
