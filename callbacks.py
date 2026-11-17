from telegram import Update
from telegram.ext import MessageHandler, Application, ContextTypes, filters
from json_man import get_services_message


async def handle_reply_keyboard_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "📖 Прайс-лист та послуги":
        await update.message.reply_html(get_services_message())

def register_handlers_callbacks(app: Application):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply_keyboard_messages))