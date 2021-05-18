from flask import Flask, request
from config import Config
from bot import bot
import telebot

server = Flask(__name__)


@server.route('/' + Config.BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=Config.BOT_WEBHOOK_URL + Config.BOT_TOKEN)
    return "!", 200
