import telegram
from telegram.ext import *

#no funciona
import requests
requests.packages.urllib3.disable_warnings() 

mi_bot = telegram.Bot(token="348031945:AAH6pTFVLYMbSrno0tIqNzWf3ZY1bLkeJfw")
mi_bot_updater = Updater(mi_bot.token)

#FUNCTIONS
def listener(bot, update):
    chat_id = update.message.chat_id
    mensaje = update.message.text
    print("CHAT_ID: "+str(chat_id)+" MENSAJE: "+mensaje)

def start(bot, update, pass_chat_data=True):
    update.message.chat_id
    bot.sendMessage(chat_id=update.message.chat_id, text="Bienvenido!")
    
#HANDLERS
start_handler = CommandHandler('start', start)
listener_handler = MessageHandler(Filters.text, listener)

#DISPATCHER
dispatcher = mi_bot_updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(listener_handler)

mi_bot_updater.start_polling()
mi_bot_updater.idle()

while True:
    pass