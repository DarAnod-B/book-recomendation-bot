import abc
import typing as tp

import telegram as tg
import telegram.ext as tg_ext

from bot import messages



class BaseHandler(abc.ABC):
    def __init__(self) -> None:
        self.user: tp.Optional[tg.User] = None

    async def __call__(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        self.user = update.effective_user
        await self.handler(update, context)

    @abc.abstractmethod
    async def handler(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplemented


class StartHandler(BaseHandler):
    async def handler(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_html(messages.start())


class HelpHandler(BaseHandler):
    async def handler(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_html(messages.help())


def setup_handlers(application: tg_ext.Application) -> None:
    # on different commands - answer in Telegram
    application.add_handler(tg_ext.CommandHandler("start", StartHandler()))
    application.add_handler(tg_ext.CommandHandler("help", HelpHandler()))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(tg_ext.MessageHandler(
    #     tg_ext.filters.TEXT & ~tg_ext.filters.COMMAND, EchoHandler))
