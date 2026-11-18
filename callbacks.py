import config
import aiocryptopay
from aiocryptopay import Networks
from telegram import Update
from telegram.ext import MessageHandler, Application, ContextTypes, filters, CallbackQueryHandler
from utils import get_services_message, load_services_2
from keyboards import get_services_keyboard, get_payment_keyboard


async def handle_reply_keyboard_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "📖 Прайс-лист та послуги":
        await update.message.reply_html(get_services_message(), reply_markup=get_services_keyboard())

async def handle_service_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    service_id = int(update.callback_query.data.split("_")[1])

    services_dict = load_services_2()
    service = services_dict.get(service_id)

    if not service:
        await update.callback_query.message.reply_text("⚠️ Послугу не знайдено.")
        return

    title = service["title"]
    price_usd = float(service["price_usd"])

    crypto = aiocryptopay.AioCryptoPay(token=config.crypto_pay_token, network=Networks.MAIN_NET)

    try:
        invoice = await crypto.create_invoice(asset="USDT", amount=price_usd, description=f"Замовлення: {title}")
    except Exception:
        await update.callback_query.message.reply_text("⚠️ Помилка створення рахунку. Спробуйте пізніше.")
        return
    finally:
        await crypto.close()

    payment_keyboard = get_payment_keyboard(pay_url=invoice.bot_invoice_url, invoice_id=invoice.invoice_id)

    await update.callback_query.message.edit_text(f"""
🧾 <b>Рахунок на оплату сформовано!</b>

🛠 Послуга: <b>{title}</b>\n
💰 Сума: <b>{price_usd} USDT</b>

Натисніть кнопку нижче для переходу до оплати:
""", reply_markup=payment_keyboard, parse_mode="HTML")

async def handle_payment_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    invoice_id = int(update.callback_query.data.split("_")[1])

    crypto = aiocryptopay.AioCryptoPay(token=config.crypto_pay_token, network=Networks.MAIN_NET)

    try:
        result = await crypto.get_invoices(invoice_ids=invoice_id)
    except Exception as e:
        await update.callback_query.answer(f"⚠️ Помилка перевірки: {e}", show_alert=True)
        return
    finally:
        await crypto.close()

    if not result:
        await update.callback_query.answer("❌ Рахунок не знайдено.", show_alert=True)
        return

    invoice = result[0] if isinstance(result, list) else result

    if invoice.status == "paid":
        await update.callback_query.answer("✅ Оплату успішно підтверджено!", show_alert=True)
        await update.callback_query.message.edit_text(
            "🎉 <b>Дякуємо! Оплата успішно пройшла.</b>\n\n"
            "Ваше замовлення прийнято в роботу. Ми зв'яжемося з вами найближчим часом!",
            parse_mode="HTML"
        )
    elif invoice.status == "active":
        await update.callback_query.answer("⏳ Оплата ще не надійшла. Спробуйте ще раз пізніше.", show_alert=True)
    else:
        await update.callback_query.answer(f"❌ Рахунок має статус: {invoice.status}", show_alert=True)

def register_handlers_callbacks(app: Application):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply_keyboard_messages))
    app.add_handler(CallbackQueryHandler(handle_service_order, pattern="^order_"))
    app.add_handler(CallbackQueryHandler(handle_payment_check, pattern="^check_"))