# Pyhton version 3.8
# python-telegram-bot~=13.1
# telegram~=0.0.1

from time import sleep
from telegram.ext import Filters , MessageHandler , Updater
from telegram.ext.dispatcher import run_async
from telegram import Bot

from env import TOKEN, BOTNAME, ADMIN_CHAT_ID, ADMIN_USER_ID

updater = None
dispatcher = None
bot = None

@run_async
def any_message(bot, message):
    bot.send_message(message.chat.id, "Hello World")

if __name__ == "__main__":
    print("Inicia el main")

    updater = Updater(token=TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    bot = Bot(token=TOKEN)

    def any_update(update, context):
        contextbot = context.bot
        if update.message and update.message.text:
            if update.message.text == "/exit" and update.message.from_user.id == ADMIN_USER_ID:
                contextbot.send_message(update.message.chat.id, "Dead.")
                updater.stop()
                print("Bot killed by /exit")
                exit()
            elif update.edited_message != None:
                any_message(contextbot, update.edited_message)
            elif update.message != None:
                any_message(contextbot, update.message)
        else:
            print("update.message is None or empty text.")
    
    core_handler = MessageHandler(Filters.text | Filters.command , any_update, run_async=True)
    dispatcher.add_handler(core_handler)

    updater.start_polling()
    try:
        print("Press Ctrl+C to exit.")
        while True:
            sleep(0.5)
        #print "Salio del raw_input(). Se cerrará."
    except KeyboardInterrupt:
        print("Ctrl-C detected. Exitting...")
    updater.stop()
    print("Bye bye.")
