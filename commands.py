import config
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from reply import start_keyboard


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(f"""
👋 <b>Вітаємо у {config.bot_name}</b>!

🤖 Створюємо сучасні <b>Telegram-боти</b> під замовлення для твого бізнесу чи ідей.

Переглядай прайс-лист, обирай потрібний формат та оформлюй замовлення в меню нижче 👇
""", reply_markup=start_keyboard())

def register_handlers_commands(app: Application):
    app.add_handler(CommandHandler("start", start_command))