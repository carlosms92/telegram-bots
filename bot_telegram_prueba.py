import telebot
import requests
requests.packages.urllib3.disable_warnings()

bot = telebot.TeleBot('348031945:AAH6pTFVLYMbSrno0tIqNzWf3ZY1bLkeJfw')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Martinez, how are you doing?")
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()