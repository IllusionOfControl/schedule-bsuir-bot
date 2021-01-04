from config import Config
import bsuir
import telebot
import logging
from flask import Flask, request


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.


bot =  telebot.TeleBot(Config.BOT_TOKEN, parse_mode=None)
server = Flask(__name__)

api = bsuir.IISBsuirApi(Config.BSUIR_USERNAME, Config.BSUIR_PASSWORD)
api.auth()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello")

@bot.message_handler(commands=['list_gradebook'])
def list_gradebook(message):
    gradebook = api.getGradebook()
    schedules = gradebook['todaySchedules']
    formated = ""
    for i in schedules:
        lessonTime = i['lessonTime']
        subject = i['subject']
        lessonType = i ['lessonType']
        formated += '*{subject}*   {lessonTime}   {lessonType}\n'.format(
            subject=subject,
            lessonTime=lessonTime,
            lessonType=lessonType
        )
    bot.reply_to(message, formated, parse_mode='markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    items = [
        telebot.types.KeyboardButton('/list_gradebook')
    ]
    for i in items:
        markup.row(i)
    bot.send_message(message, reply_markup=markup)


@server.route('/' + Config.BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=Config.BOT_WEBHOOK_URL + Config.BOT_TOKEN)
    return "!", 200


#bot.set_webhook(url=Config.BOT_WEBHOOK_URL)