import abc
import typing as tp
from enum import Enum

import telegram as tg
import telegram.ext as tg_ext

from bot import messages


class ButtonName(Enum):
    searchSimilarBooks = "Найти похожую книгу."
    searchRecommendations = "Порекомендовать книгу."


class BaseHandler(abc.ABC):
    def __init__(self) -> None:
        self.user: tp.Optional[tg.User] = None

    async def __call__(
        self, update: tg.Update, context: tg_ext.ContextTypes
    ) -> None:
        self.user = update.effective_user
        await self.handler(update, context)

    @abc.abstractmethod
    async def handler(
        self, update: tg.Update, context: tg_ext.ContextTypes
    ) -> None:
        raise NotImplemented


class StartHandler(BaseHandler):
    async def handler(
        self, update: tg.Update, context: tg_ext.ContextTypes
    ) -> None:
        input_data = {
            'user_name': self.user.first_name
        }
        buttons = [[tg.KeyboardButton(ButtonName.searchSimilarBooks.value)], [
            tg.KeyboardButton(ButtonName.searchRecommendations.value)]]

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Welcome to my bot! q", reply_markup=tg.ReplyKeyboardMarkup(buttons))
        await update.message.reply_html(messages.Start.text.value.format(**input_data))


class HelpHandler(BaseHandler):
    async def handler(
        self, update: tg.Update, context: tg_ext.ContextTypes
    ) -> None:
        await update.message.reply_html(messages.Help.text.value)


class ModelHandler(BaseHandler):
    async def handler(
        self, update: tg.Update, context: tg_ext.ContextTypes
    ) -> None:
        await update.message.reply_html(messages.Help.text.value)


def setup_handlers(application: tg_ext.Application) -> None:
    # on different commands - answer in Telegram
    application.add_handler(tg_ext.CommandHandler("start", StartHandler()))
    application.add_handler(tg_ext.CommandHandler("help", HelpHandler()))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(tg_ext.MessageHandler(
    #     tg_ext.filters.TEXT & ~tg_ext.filters.COMMAND, EchoHandler))
