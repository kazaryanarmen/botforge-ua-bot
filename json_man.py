import json
import os


JSON_FILE = "services.json"


def load_services():  
    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data.get("services", [])
        except json.JSONDecodeError:
            return []


def add_service(title, category, description, delivery_time_days, price_usd, price_uah):
    services = load_services()

    new_id = len(services) + 1

    new_service = {
        "id": new_id,
        "title": title,
        "category": category,
        "description": description,
        "delivery_time_days": delivery_time_days,
        "price_usd": price_usd,
        "price_uah": price_uah,
    }

    services.append(new_service)

    data = {"services": services}

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Послугу «{title}» успішно додано до файлу {JSON_FILE}!")

def get_services_message() -> str:
    if not os.path.exists(JSON_FILE):
        return (
            "📋 <b>Прайс-лист наразі оновлюється.</b>\n\nСлідкуйте за оновленнями! 🚀"
        )

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            services = data.get("services", [])
        except json.JSONDecodeError:
            return "⚠️ Виникла помилка при читанні прайс-листа."

        if not services:
            return "📋 У прайс-листі поки немає активних послуг."


        message = "📋 <b>Актуальний прайс-лист BotForge:</b>\n\n"

        for service in services:
            title = service.get("title", "Послуга")
            price_usd = service.get("price_usd", 0)
            price_uah = service.get("price_uah", 0)
            days = service.get("delivery_time_days", 1)
            description = service.get("description", "")

        message += f"🛠 <b>{title}</b>\n"
        message += (
            f"💰 <b>Ціна:</b> ${price_usd} (~{price_uah} грн)\n"
            f"⏱ <b>Термін:</b> від {days} днів\n"
        )

        if description:
            message += f"📝 <i>{description}</i>\n"


        message += "\n" + "—" * 20 + "\n\n"
        message += "👇 <i>Обирай потрібну послугу та зв'язуйся для замовлення!</i>"

        return message