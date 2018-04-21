#Bot conversacion

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, 
                        Filters, RegexHandler, ConversationHandler)
                
import logging

#Habilitamos el log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Edad', 'Color favorito'], 
                ['Numero de hermanos', 'Algunas cosas...'],
                ['Completado']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def facts_to_str(user_data):
    facts = list()
    
    for key,value in user_data.items():
        facts.append('{} - {}'.format(key, value))
        
    return "\n".join(facts).join(['\n', '\n'])
    
def start(bot, update):
    update.message.reply_text(
        "Hola, soy un bot de conversacion."
        "Por que no me dices algo sobre ti",
        reply_markup=markup)
        
    return CHOOSING
    
def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(
        'Tu {}? Si, me encantaria escuchar sobre eso!'.format(text.lower()))

    return TYPING_REPLY
    
def custom_choice(bot, update):
    update.message.reply_text(
        'Muy bien, por favor envieme la categoria primero, '
        'por ejemplo, "habilidad mas impresionante"')
        
    return TYPING_CHOICE
    
def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    
    update.message.reply_text(
        "Ordenado! Para que lo sepas, esto es lo que ya me dijiste:"
        "{}"
        "Puedes decirme mas o cambiar tu opinion sobre algo.".format(
            facts_to_str(user_data)), reply_markup=markup)
            
    return CHOOSING
    
def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']
        
    update.message.reply_text(
        "Aprendi esto sobre ti:"
        "{}"
        "Hasta la proxima vez".format(facts_to_str(user_data)))
        
    user_data.clear()
    return ConversationHandler.END
    
def error(bot, update, error):
    #Log errors causados por Updates.
    logger.warning('La actualizacion "%s" provoco el error "%s"', update, error)
    
def main():
    #Crea el actualizador le pasa el token del bot
    updater = Updater("348031945:AAH6pTFVLYMbSrno0tIqNzWf3ZY1bLkeJfw")
    
    #Obtener el dispatcher para registrar los controladores
    dp = updater.dispatcher
    
    #Agrega manejador de conversacion con los estados GENDER, PHOTO, LOCATION y BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        
        states={
            CHOOSING: [RegexHandler('^(Edad|Color favorito|Numero de hermanos)$',
                                    regular_choice,
                                    pass_user_data=True),
                        RegexHandler('^Algunas cosas...$',
                                    custom_choice),
                        ],
                        
            TYPING_CHOICE: [MessageHandler(Filters.text,
                                            regular_choice,
                                            pass_user_data=True),
                            ],
                            
            TYPING_REPLY: [MessageHandler(Filters.text,
                                            received_information,
                                            pass_user_data=True),
                            ],
                            
            
        },
        
        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )
    
    dp.add_handler(conv_handler)
    
    # log all errors
    dp.add_error_handler(error)
    
    # Empieza el bot
    updater.start_polling()
    
    #  Ejecuta el bot hasta que se presione Ctrol-C o el proceso reciba SIGINT,
    # SIGTERM o SIGABRT, Esto debe usarse la mayor parte del tiempo, ya que
    # start_polling() no bloquea y detendra el bot con gracia.
    updater.idle()
    
if __name__ == '__main__':
    main()