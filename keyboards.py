from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from utils import load_services_2


def start_keyboard():
    keyboard = [
        [KeyboardButton(text="🚀 Замовити бота")],
        [KeyboardButton(text="📖 Прайс-лист та послуги")]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_services_keyboard():
    services_dict = load_services_2()
    keyboard = []

    for service_id, service_data in services_dict.items():
        title = service_data["title"]
        price_usd = service_data["price_usd"]

        button_text = f"{title} - ${price_usd}"
        callback_data = f"order_{service_id}"

        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard(pay_url: str, invoice_id: int):
    keyboard = [
        [InlineKeyboardButton("💳 Оплатити через CryptoBot", url=pay_url)],
        [InlineKeyboardButton("🔄 Перевірити оплату", callback_data=f"check_{invoice_id}")]
    ]

    return InlineKeyboardMarkup(keyboard)