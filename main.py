import config
import logging
from telegram import Update
from telegram.ext import Application
from commands import register_handlers_commands
from callbacks import register_handlers_callbacks


logging.basicConfig(level=logging.INFO)


def main() -> None:
    app = Application.builder().token(token=config.bot_token).build()

    register_handlers_commands(app)
    register_handlers_callbacks(app)


    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()