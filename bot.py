from config import Config
import bsuir
import telebot
import logging


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.


bot =  telebot.TeleBot(Config.BOT_TOKEN, parse_mode=None)
api = bsuir.IISBsuirApi()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello")

@bot.message_handler(commands=['list_gradebook'])
def list_gradebook(message):
    gradebook = None
    try:
        gradebook = api.getGradebook()
    except bsuir.AuthRequired as e:
        api.auth(Config.BSUIR_USERNAME, Config.BSUIR_PASSWORD)
        gradebook = e.try_method()
        
    schedules = gradebook['todaySchedules']
    formated = ""
    for i in schedules:
        lessonTime = i['lessonTime']
        subject = i['subject']
        lessonType = i ['lessonType']
        formated += "{subject} {lessonTime} {lessonType}\n".format(
            subject=subject,
            lessonTime=lessonTime,
            lessonType=lessonType
        )
    bot.reply_to(message, formated)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    items = [
        telebot.types.KeyboardButton('/list_gradebook')
    ]
    for i in items:
        markup.row(i)
    bot.send_message(message, reply_markup=markup)


#bot.set_webhook(url=Config.BOT_WEBHOOK_URL)