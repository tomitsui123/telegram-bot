import configparser
from io import BytesIO

import requests
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes

from modules.weather_service import get_weather_info_from_observatory, process_rain_graph, get_typhoon_info
from utils.logger import get_logger

logger = get_logger()


def polling_handler(update, context):
    print("polling handler")
    chat_id = update.effective_chat.id
    if len(context.args) < 3:
        return context.bot.send_message(
            chat_id=chat_id,
            text="入野先啦仆街 ".format(update.effective_user.mention_markdown()))
    question, *questions = context.args
    message = context.bot.send_poll(
        update.effective_chat.id,
        question,
        questions,
        is_anonymous=False,
    )
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)
    context.bot.pinChatMessage(chat_id=chat_id, message_id=message.message_id)


def polling_multiple_handler(update, context):
    chat_id = update.effective_chat.id
    if not len(context.args):
        return context.bot.send_message(
            chat_id=chat_id,
            text="入野先啦仆街")
    question, *questions = context.args
    message = context.bot.send_poll(
        update.effective_chat.id,
        question,
        questions,
        is_anonymous=False,
        allows_multiple_answers=True
    )
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)
    context.bot.pinChatMessage(chat_id=chat_id, message_id=message.message_id)


def weather_handler(update, context):
    chat_id = update.effective_chat.id
    logger.info("Getting data from observatory")
    today_weather = get_weather_info_from_observatory()
    try:
        process_rain_graph()
        context.bot.send_message(chat_id=chat_id, text=today_weather, parse_mode="MarkdownV2")
        context.bot.send_animation(update.effective_chat.id, open('./radar.gif', 'rb'))
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="天文台大爆炸呀 要再run過")


def typhoon_handler(update, context):
    typhoon_info_list = get_typhoon_info()
    for info in typhoon_info_list:
        res = requests.get(info["typhoon_img_url"])
        img = BytesIO(res.content)
        context.bot.send_photo(update.effective_chat.id, img, info["name"])


def on9_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="on9")


async def exchange_rate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: pull the exchange rate info (ALDO)
    await update.message.reply_html(
        rf"Aldo 未做 {update.message.from_user.first_name}",
    )


def get_command_handlers():
    handlers = {
        "polling": polling_handler,
        "polling_multiple": polling_multiple_handler,
        "weather": weather_handler,
        "typhoon": typhoon_handler,
        "on9": on9_handler,
        "exchange_rate": exchange_rate_handler
    }
    res = []
    for (command, handler) in handlers.items():
        res.append(CommandHandler(command, handler))
    return res


def main() -> None:
    config = configparser.ConfigParser()
    config.read('./config.ini')
    token = config.get("CONFIG", "token")
    application = Application.builder().token(token).build()
    for command_handler in get_command_handlers():
        application.add_handler(command_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()