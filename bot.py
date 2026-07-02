import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
import payments

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message and payment options"""
    keyboard = [
        [InlineKeyboardButton("💳 Buy Premium ($10)", callback_data="buy_premium")],
        [InlineKeyboardButton("📦 View Products", callback_data="view_products")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Use the buttons below to make a purchase.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()

    if query.data == "buy_premium":
        # Create Stripe checkout session and get payment link
        session_url = payments.create_checkout_session(
            price_id=payments.PRODUCT_PRICE_ID,
            user_id=query.from_user.id
        )
        await query.edit_message_text(
            f"Click the link below to complete your payment:\n\n{session_url}\n\n"
            "After payment, you'll receive a confirmation."
        )
    elif query.data == "view_products":
        await query.edit_message_text(
            "📦 **Available Products:**\n"
            "• Premium Subscription - $10/month\n"
            "More products coming soon!"
        )

def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
