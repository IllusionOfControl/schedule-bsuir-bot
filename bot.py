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
        auditory = i['auditory'][0]
        response += '*{subject}*   {lessonTime}   {lessonType}   _{auditory}_\n'.format(
            subject=subject,
            lessonTime=lesson_time,
            lessonType=lesson_type,
            auditory=auditory
        )
    else:
        response = 'There is no schedule for today! :D'
    bot.send_message(message.chat.id, response, parse_mode='markdown')


@bot.message_handler(commands=['list_at'])
def list_schedule_at(message):
    bot.send_message(message.chat.id, 'Input pls the target date')
    bot.register_next_step_handler(message, process_date_step)


def process_date_step(message):
    schedule = api.get_schedule()
    response = ''

    if len(message.text) < 2:
        bot.send_message(message.chat.id, 'Please enter the correct value (dd.mm)\nFor example 01 or 01.01')
        return

    date = message.text
    for i in schedule['examSchedules']:
        if i['weekDay'].startswith(date):
            for j in i['schedule']:
                lesson_time = j['lessonTime']
                subject = j['subject']
                lesson_type = j['lessonType']
                auditory = j['auditory'][0]
                response += '*{subject}*   {lessonTime}   {lessonType}   _{auditory}_\n'.format(
                    subject=subject,
                    lessonTime=lesson_time,
                    lessonType=lesson_type,
                    auditory=auditory
                )
            break
    else:
        response = 'the schedule for this day was not found :('
    bot.send_message(message.chat.id, response, parse_mode='markdown')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    response = 'I don\'t understand {text}. Maybe try the help page at /help'.format(
        text=message.text
    )
    bot.send_message(message.chat.id, text=response)
