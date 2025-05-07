# Pyhton version 3.8
# python-telegram-bot~=13.1
# telegram~=0.0.1

from time import sleep
from telegram.ext import Filters , MessageHandler , Updater
from telegram.ext.dispatcher import run_async
from telegram import Bot
import dotenv
import os

# Load 'env' variables from file
dotenv.load_dotenv('.env')
TOKEN = os.environ['TOKEN']
ADMIN_CHAT_ID = int(os.environ['ADMIN_CHAT_ID'])
ADMIN_USER_ID = int(os.environ['ADMIN_USER_ID'])

running = True
updater = None
dispatcher = None
bot = None

CURRENCY = '€' # Anyway app uses cents number system for displaying.
FORCE_CENTS = True # If it's true, stops saving passed amounts less than one cent

def any_message(bot, message):
    global running
    text = message.text
    chat_id = message.chat.id

    # Kill bot
    if text == "/exit" and (message.from_user.id == ADMIN_USER_ID or chat_id == ADMIN_CHAT_ID):
        bot.send_message(chat_id, "Bot is shutting down...")
        running = False  # Set the flag to False to break the loop
        print("Bot stopped by /exit command.")
        return  # Exit the function to avoid further processing

    file_path = f'{data_folder}/{chat_id}.txt'
    # Create file if it does not exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('0')
            print(f'Created {file_path}')
            f.close()

    if text.startswith('+') or text.startswith('-'):
        # Get value from file or start new one
        with open(file_path, 'r') as f:
            try:
                value = float(f.read())
            except ValueError as e:
                print(f'File error: {e}, handled as 0')
                value = float(0)
            f.close()
        try:
            
            text = text.replace(CURRENCY, '') # Remove currency symbol  
            text = text.replace(' ', '') # Remove space references
            text = text.replace(',', '.') # Replace ',' for '.'

            # Ignore negligible amounts
            if FORCE_CENTS == True:
                if "." in text:
                    text = text.split(".")
                    text[1] += "00"
                    text = text[0] + '.' + text[1][:2]

            old_value = value
            value = value + float(text) # Change the variable
            decimal_value = int(value) # Get the non fractional part of the number

            # Get the cents part of the number
            assert(isinstance(value, float))
            cents_string = (str(value) + "00").split('.')[1]
            cents_string = cents_string[0] + cents_string[1]

            # Output text creation
            output_text = str(decimal_value) + '.' + cents_string + ' ' + CURRENCY
            if CURRENCY == '€':
                # Germany standarts
                output_text = output_text.replace('.00', '.—')
                if decimal_value == 0:
                    output_text = output_text.replace('0.', '—.')
            
            bot.send_message(message.chat.id, output_text) # Send the variable
        except ValueError as e:
            print(f'Value error parsing data. Error: {e}')
            return # Do not keep going

        # Store new value in order to perform future actions
        with open(file_path, 'w') as f:
            f.write(str(value))
            f.close()

if __name__ == "__main__":
    data_folder = 'storage'
    try:
        os.mkdir(data_folder)
    except Exception as e:
        ...
    # Check os permissions for file editing, necessary.
    assert(os.access(f"{data_folder}", os.R_OK))
    assert(os.access(f"{data_folder}", os.W_OK))

    print("Hi.")

    # Using library to launch the bot
    updater = Updater(token=TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    bot = Bot(token=TOKEN)
    def any_update(update, context):
        contextbot = context.bot
        if update.message and update.message.text:
            if update.edited_message != None:
                pass # The code do nothing with edited messages for now. However it cannot access to the previous text of the edition.
            elif update.message != None:
                any_message(contextbot, update.message)
        else:
            pass
    core_handler = MessageHandler(Filters.text | Filters.command , any_update, run_async=True)
    dispatcher.add_handler(core_handler)
    updater.start_polling()
    try:
        print("Press Ctrl+C to exit.")
        while running > 0:
            sleep(running)
    except KeyboardInterrupt:
        print("\nCtrl-C detected. Exiting...")
    updater.stop()
    print("Bye bye.")
