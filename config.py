import os
from dotenv import load_dotenv


load_dotenv()


bot_token = os.getenv("BOT_TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))

bot_name = "Bot Forge"