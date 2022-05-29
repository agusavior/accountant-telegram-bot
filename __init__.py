# Pyhton version 3.8
# python-telegram-bot~=13.1
# telegram~=0.0.1

from time import sleep
from telegram.ext import Filters , MessageHandler , Updater
from telegram.ext.dispatcher import run_async
from telegram import Bot
import os

from env import TOKEN, BOTNAME, ADMIN_CHAT_ID, ADMIN_USER_ID

updater = None
dispatcher = None
bot = None

CURRENCY = '€'

@run_async
def any_message(bot, message):
    text = message.text
    chat_id = message.chat.id

    if text.startswith('+') or text.startswith('-'):
        # Create storage file if does not exist
        try:
            os.mkdir('storage')
        except Exception as e:
            print(f'Error creating storage folder. Error: {e}')
        
        # The file where we recall the debt number
        file_path = f'storage/{chat_id}.txt'

        # Create data file if it does not exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('0')
            print(f'Created a new data file {file_path} with value of 0 cents.')

        # Get cents of data file
        with open(file_path, 'r') as f:
            current_cents = int(f.read())

        try:
            # Remove currency symbol
            text = text.replace('€', '')

            # Replace ',' for '.'
            text = text.replace(',', '.')

            # Update cents
            centsdiff = int(float(text) * 100)
            new_cents = current_cents + centsdiff
            output_text = '{:.2f} {}'.format(new_cents / 100.0, CURRENCY)
            
            # Germany standarts
            output_text = output_text.replace('.00', '.—')
            if output_text.startswith('0'):
                output_text = output_text.replace('0.', '—.')
            
            bot.send_message(message.chat.id, output_text)
        except ValueError as e:
            print(f'Value error parsing data. Error: {e}')

            # Do not keep going
            return

        # Store new cents value in order to perform future actions
        with open(file_path, 'w') as f:
            f.write(str(new_cents))

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
