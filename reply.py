from telegram import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard():
    keyboard = [
        [KeyboardButton(text="🚀 Замовити бота")],
        [KeyboardButton(text="📖 Прайс-лист та послуги")]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)