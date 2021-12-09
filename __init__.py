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

CURRENCY = '€'

# Dict where keys are chat ids, and values are int
cents_of = dict()

@run_async
def any_message(bot, message):
    text = message.text
    chat_id = message.chat.id

    if text.startswith('+') or text.startswith('-'):
        if chat_id not in cents_of:
            cents_of[chat_id] = 0

        current_cents = cents_of[chat_id]

        try:
            # Update cents
            centsdiff = int(float(text) * 100)
            new_cents = current_cents + centsdiff
            cents_of[chat_id] = new_cents
            output_text = '{:.2f} {}'.format(new_cents / 100.0, CURRENCY)
            
            # Germany standarts
            output_text = output_text.replace('.00', '.—')
            if output_text.startswith('0'):
                output_text = output_text.replace('0.', '—.')
            
            bot.send_message(message.chat.id, output_text)
        except ValueError as e:
            pass

if __name__ == "__main__":
    print("Hi.")

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
            sleep(500)
    except KeyboardInterrupt:
        print("Ctrl-C detected. Exitting...")
    updater.stop()
    print("Bye bye.")
