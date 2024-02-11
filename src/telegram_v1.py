import telegram.ext
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN")

updater =telegram.ext.Updater(token, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Hello")

def help(update, context):
    update.message.reply_text(
    """
    /start --> Welcome to channel

    """
    )

start_value=telegram.ext.CommandHandler("start", start)
dispatcher.add_handler(start_value)

updater.start_polling()
updater.idle()