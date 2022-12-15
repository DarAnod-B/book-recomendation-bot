import os
import logging
import telegram.ext as tg_ext
from bot import handlers

bot_token = os.environ.get('BookRecBotToken')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = tg_ext.Application.builder().token(bot_token).build()
    handlers.setup_handlers(application)
    application.run_polling()


if __name__ == "__main__":
    main()
