import logging
import os
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask, jsonify
import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app for webhook
flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return jsonify({"status": "alive", "bot": "running"})

def run_flask():
    """Run Flask server in background"""
    port = int(os.getenv("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    keyboard = [
        [InlineKeyboardButton("💳 Buy Premium ($10)", callback_data="buy")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 **Welcome to Stripe Provider Bot!**\n\n"
        "I can process payments using Stripe.\n"
        "Use the buttons below to get started.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    logger.info(f"User {update.effective_user.id} started the bot")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "buy":
        await query.edit_message_text(
            "💳 **Payment Processing**\n\n"
            "Stripe integration is ready!\n"
            "Add your Stripe product ID to enable payments."
        )
    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ **About This Bot**\n\n"
            "This bot handles Stripe payments.\n"
            "Built with Python + python-telegram-bot."
        )
    logger.info(f"Button clicked: {query.data} by user {query.from_user.id}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Run the bot"""
    # Check token
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN is missing! Set it in environment variables.")
        return
    
    logger.info("🚀 Starting bot...")
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"✅ Flask server running on port {os.getenv('PORT', 8080)}")
    
    # Create bot application
    app = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    
    # Start bot
    logger.info("✅ Bot is polling for messages...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
