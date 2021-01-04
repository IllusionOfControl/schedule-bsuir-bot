from bot import bot, server
import os

if __name__ == "__main__":
    #bot.polling()
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))