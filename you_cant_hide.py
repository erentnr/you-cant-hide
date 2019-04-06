from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import update_data
import datetime
import requests
import json
import os


def is_outdated():

    file_path = 'data.json'
    exists = os.path.isfile(file_path)
    current_time = datetime.datetime.today()
    min_time_diff = datetime.timedelta(hours = 12)

    if exists:
        last_updated = datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime)
        if (last_updated + min_time_diff) < current_time:
            return True
        else:
            return False
    else:
        return True


def get_instructor_data(bot, update):
    search_name = update.message.text
    chat_id = update.message.chat_id
    exists = os.path.isfile('data.json')

    if exists:
        with open('data.json', 'r') as f:
            instructor_dict = json.load(f)
            try:
                msg = ''
                for crn in instructor_dict[search_name]:
                    msg += '<b>{}</b>\n{}\n{}\n{}\n\n'.format(crn[2], crn[4], crn[5], crn[3])
                bot.send_message(parse_mode='HTML', chat_id=chat_id, text=msg)
            except:
                msg = "The name is wrong or doesn't exist. Try again."
                bot.send_message(chat_id=chat_id, text=msg)
    else:
        msg = "Please update the schedules with /update"
        bot.send_message(chat_id=chat_id, text=msg)


def data_update(bot, update):
    chat_id = update.message.chat_id
    outdated = is_outdated()

    if outdated:
        msg = "This usually takes 2 minutes. Please wait."
        bot.send_message(chat_id=chat_id, text=msg)
        update_data.update_instructor_data()
        msg = "The data is now updated!"
        bot.send_message(chat_id=chat_id, text=msg)
    else:
        msg = "Schedules are already updated."
        bot.send_message(chat_id=chat_id, text=msg)


def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Hi. Type the instructor's full name in a nice format.\n\nExample: Mehmet Nazmi Postacıoğlu \n\nIf you think the schedules is outdated, just type /update.")


def main():
    TOKEN = 'YOUR TOKEN'
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('update', data_update))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_instructor_data))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
