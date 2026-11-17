import config
from telegram import Update
from telegram.ext import Application


def main() -> None:
    app = Application.builder().token(token=config.bot_token).build()

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()