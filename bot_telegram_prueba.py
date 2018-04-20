import telegram
from telegram.ext import *

mi_bot = telegram.Bot(token="348031945:AAH6pTFVLYMbSrno0tIqNzWf3ZY1bLkeJfw")
mi_bot_updater = Updater(mi_bot.token)

def start(bot, update, pass_chat_data=True):
    update.message.chat_id
    bot.sendMessage(chat_id=update.message.chat_id, text="Bienvenido!")
    
start_handler = CommandHandler('start', start)

dispatcher = mi_bot_updater.dispatcher
dispatcher.add_handler(start_handler)

mi_bot_updater.start_polling()
mi_bot_updater.idle()

while True:
    pass