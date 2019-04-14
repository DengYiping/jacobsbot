from telegram.ext import Updater, CommandHandler
from apetito_parser import find_today as find_menu_today
from pymongo import MongoClient
from telegram.ext.dispatcher import run_async

APETITO_MENU = 'menu.pdf'

def hello(bot, update):
    name = update.message.from_user.first_name

    update.message.reply_text(f'Hello {name}, welcome to Jacobs Bot!\n' +
                              'To find the menu, please type /menu,\n' +
                              'To find people, please type /people NAME_OF_THE_PERSON,\nEnjoy!')
@run_async
def menu(bot, update):
    # send back the apetito menu
    chat_id = update.message.chat_id
    # bot.sendDocument(chat_id = chat_id, document = open(APETITO_MENU, 'rb'))

    # get the image for lunch and for dinner
    lunch, dinner = find_menu_today()
    bot.send_message(chat_id = chat_id, text = 'for lunch today:')
    bot.send_photo(chat_id = chat_id, photo = open(lunch, 'rb'))
    bot.send_message(chat_id = chat_id, text = 'for dinner today:')
    bot.send_photo(chat_id = chat_id, photo = open(dinner, 'rb'))

@run_async
def people(bot, update, args):
    limit = 5
    chat_id = update.message.chat_id

    collection = MongoClient('mongodb://localhost:27017/')['jacobs']['jpeople']

    query_str = " ".join(args)
    print(f'query for people: {query_str}')

    results = collection.find({'$text': {'$search': query_str}})

    # number of results
    reply_count = 0

    msgs = []
    for result in results:
        if reply_count >= limit:
            break

        first_name = result['firstName']
        last_name = result['lastName']
        email = result['email']
        year = result['year']
        major = result['majorShort']
        college = result['college']
        room = result['room']
        country = result['country']

        reply_str = f'Name: {first_name} {last_name}\n'
        reply_str += f'Email: {email}, \nYear: {year},\nMajor: {major}, \nCountry: {country}\n'
        reply_str += f'College: {college},\nRoom: {room}'
        msgs.append(reply_str)

    for msg in msgs:
        bot.send_message(chat_id = chat_id, text = msg)


def main():
    updater = Updater('767966885:AAEoNaEdhokCm37KgjjJub49TnulDcBvAls', workers = 16)
    updater.dispatcher.add_handler(CommandHandler(['hello', 'start', 'help'], hello))
    updater.dispatcher.add_handler(CommandHandler(['menu'], menu))
    updater.dispatcher.add_handler(CommandHandler('people', people, pass_args = True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
