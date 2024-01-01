import configparser
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update
from telegram.ext import ContextTypes, Application, MessageHandler, filters

from modules.currency_module import get_exchange_rate_msg
from modules.meal_module import contains_meal_info
from modules.nba_module import get_livestream_link, get_nba_score_table
from modules.translate_module import is_foreign_language, google_translate
from utils.logger import get_logger

logger = get_logger()
config = configparser.ConfigParser()
config.read('../config.ini')


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    responses = {
        "三色豆": "@grammarho57 on9 發仔",
        "@grammarho57": "@grammarho5l7 on9 發仔",
        "莫忽": "@grammarho57 on9 @莫忽",
        "水族館": "on9 @莫忽",
        "禿頭": "on9 @莫忽",
        "過兒": "留日啦仆街",
        "回家": "留日啦仆街",
        "日本": "留日啦仆街",
    }

    if contains_meal_info(update.message.text):
        response = "又唔叫" + str(update.message.from_user.first_name)
    elif "NBA link".lower() in update.message.text.lower():
        response = get_livestream_link()
    elif "NBA score".lower() in update.message.text.lower():
        response = "```" + get_nba_score_table() + "```"
    elif "exchange rate".lower() in update.message.text.lower():
        await _exchange_rate_scheduler(update)
        return
    else:
        response = next((resp for key, resp in responses.items() if key in update.message.text), None)

    if response:
        await update.message.reply_text(text=response, parse_mode="MarkdownV2")


async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    shown_msg = update.message.caption
    if contains_meal_info(shown_msg):
        await update.message.reply_text("又唔叫"
                                        + str(update.message.from_user.first_name))


is_scheduled = False
scheduler = AsyncIOScheduler(timezone="Hongkong")


async def exchange_rate_sender(reply_text):
    msg = get_exchange_rate_msg()
    logger.info("sent exchange rate")

    await reply_text(text=msg)


async def _exchange_rate_scheduler(update: Update):
    global is_scheduled
    if "start".lower() in update.message.text.lower() and not is_scheduled:
        hour = config.get("CONFIG", "scheduled_at_in_hour")
        minute = config.get("CONFIG", "scheduled_at_in_minute")
        await update.message.reply_text(f"Currency reporter is scheduled at {hour}:{minute} everyday")
        scheduler.add_job(exchange_rate_sender, "cron",
                          day_of_week="*",
                          hour=hour,
                          minute=minute,
                          args=[update.message.reply_text])
        # scheduler.add_job(exchange_rate_sender, "interval",
        #                   seconds=10,
        #                   args=[update.message.reply_text])
        logger.info("[start] exchange rate scheduler")
        scheduler.start()
        is_scheduled = True
    if "end".lower() in update.message.text.lower() and is_scheduled:
        logger.info("[end] exchange rate scheduler")
        await update.message.reply_text(f"Currency reporter has been shut down")
        scheduler.shutdown()
        is_scheduled = False


def main() -> None:
    token = config.get("CONFIG", "token")
    application = Application.builder().token(token).build()
    application.add_handler(MessageHandler(filters.TEXT, message_handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
