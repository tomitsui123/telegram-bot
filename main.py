#!/usr/bin/python
import configparser
from telegram import Update
from telegram.ext import MessageHandler, filters, Application
from controllers.command_controller import get_command_handlers
from controllers.message_controller import message_handler, image_handler
from utils.logger import get_logger

config = configparser.ConfigParser()
config.read('config.ini')
token = config.get("CONFIG", "token")
logger = get_logger()

if __name__ == '__main__':
    logger.info("Bot started")
    application = Application.builder().token(token).build()
    for command_handler in get_command_handlers():
        application.add_handler(command_handler)
    application.add_handler(MessageHandler(filters.TEXT, message_handler))
    application.add_handler(MessageHandler(filters.PHOTO, image_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
