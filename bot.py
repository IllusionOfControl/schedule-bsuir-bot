from config import Config
import bsuir
import telebot
import logging


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(Config.BOT_TOKEN, parse_mode=None)

api = bsuir.IISBsuirApi(Config.BSUIR_USERNAME, Config.BSUIR_PASSWORD)
api.auth()

commands = {
    'start': 'Get used to the bot',
    'list': 'Displaying the schedule for the current day',
    'list_at': 'Displaying the schedule for the target date'
}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, {}!'.format(message.from_user.first_name))


@bot.message_handler(commands=['help'])
def start(message):
    cid = message.chat.id
    help_text = 'The following commands are available: \n'
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['list'])
def list_schedule(message):
    schedule = api.get_schedule()
    schedules = schedule['todaySchedules']
    response = ''

    for i in schedules:
        lesson_time = i['lessonTime']
        subject = i['subject']
        lesson_type = i['lessonType']
        response += '*{subject}*   {lessonTime}   {lessonType}\n'.format(
            subject=subject,
            lessonTime=lesson_time,
            lessonType=lesson_type
        )
    else:
        response = 'There is no schedule for today! :D'
    bot.reply_to(message, response, parse_mode='markdown')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    items = [
        telebot.types.KeyboardButton('/list_gradebook')
    ]
    for i in items:
        markup.row(i)
    bot.send_message(message, reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

# bot.set_webhook(url=Config.BOT_WEBHOOK_URL)
