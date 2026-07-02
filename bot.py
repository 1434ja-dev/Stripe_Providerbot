import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
import stripe

stripe.api_key = STRIPE_SECRET_KEY  # import this too

# Add this to run both the bot AND webhook server
from payments import app as webhook_app
import threading
import os

def run_webhook():
    webhook_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Buy Premium ($10)", callback_data="buy_premium")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Click below to purchase.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_premium":
        # You'll add Stripe session creation here
        await query.edit_message_text(
            "Processing payment... (Stripe integration coming soon)"
        )

def main():
    # Start webhook server in background thread
    threading.Thread(target=run_webhook, daemon=True).start()
    
    # Start bot
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running on Railway!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
