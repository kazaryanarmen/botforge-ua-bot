import os
from dotenv import load_dotenv


load_dotenv()


bot_token = os.getenv("BOT_TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))

crypto_pay_token = os.getenv("CRYPTO_PAY_TOKEN")

bot_name = "Bot Forge"