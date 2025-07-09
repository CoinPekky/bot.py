import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, 
    CallbackQueryHandler, MessageHandler, Filters
)

# Get token from Render environment variables
TOKEN = os.environ.get('TOKEN')
TWITTER_URL = "https://twitter.com/AvalaunchApp"
FACEBOOK_URL = "https://web.facebook.com/search/top/?q=presale%20marketing%20agancy%20groups"
TELEGRAM_CHANNEL = "https://t.me/your_channel"  # CHANGE TO YOUR ACTUAL CHANNEL

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🌟 Join Channel", url=TELEGRAM_CHANNEL)],
        [InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_URL)],
        [InlineKeyboardButton("👍 Follow Facebook", url=FACEBOOK_URL)],
        [InlineKeyboardButton("💳 Submit SOL Wallet", callback_data="submit_wallet")]
    ]
    update.message.reply_text(
        "🎉 Welcome to ConPekky Airdrop!\n\n"
        "Complete these steps:\n"
        "1. Join our Telegram channel\n"
        "2. Follow our Twitter\n"
        "3. Like our Facebook page\n"
        "4. Submit SOL wallet\n",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "submit_wallet":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Please send your SOL wallet address:"
        )
        context.user_data['awaiting_wallet'] = True

def handle_wallet(update: Update, context: CallbackContext) -> None:
    if 'awaiting_wallet' not in context.user_data:
        return
        
    wallet = update.message.text.strip()
    update.message.reply_text(
        "🎉 Congratulations! You've passed the ConPekky airdrop!\n\n"
        "100 SOL is on its way to your wallet!\n\n"
        "Note: This is a test - no actual SOL will be sent.\n"
        "Hope you didn't cheat the system 😉"
    )
    del context.user_data['awaiting_wallet']

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))
    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
