import sqlite3
from sqlite3 import Error

import telebot


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print('Connection to SQLite DB successful')
    except Error as err:
        print('Error: ', err)

    return conn


def create_db(name):
    fh = None
    try:
        fh = open(name, mode='w')
    except EnvironmentError as err:
        print('Error: ', err)
    finally:
        fh.close()


create_db('test_sql.sqlite')


def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE polls
                 (name text, answer_1 text, answer_2)''')
    conn.commit()
    conn.close()


def main():
    bot = telebot.TeleBot('1015689433:AAGvZzz7V1B0igSY8-3PtbitmdNWuS658Fg')

    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard1.row('Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4')

    keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard2.row('Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4')

    conn = create_connection('test_sql.sqlite')
    create_tables(conn)

    @bot.message_handler(content_types=['text'])
    def start_message(message):
        if message.text == '/start':
            bot.send_message(message.chat.id, 'Спасибо что согласились учавствовать в данном опросе!',
                             reply_markup=keyboard1)
            bot.send_message(message.chat.id, 'Вопрос 1: ', reply_markup=keyboard1)
            answer_2 = message.text
            bot.register_next_step_handler(message, second_question)

    def second_question(message):
        bot.send_message(message.chat.id, 'Вопрос 2: ', reply_markup=keyboard2)
        answer_1 = message.text
        bot.register_next_step_handler(message, save_sequence, answer_1=answer_1)

    def save_sequence(message, answer_1=None):
        answer_2 = message.text
        name = '{first_name} {last_name}'.format(first_name=message.from_user.first_name,
                                                 last_name=message.from_user.last_name)
        values = (name, answer_1, answer_2)

        conn = create_connection('test_sql.sqlite')
        cur = conn.cursor()
        cur.execute('INSERT INTO polls(name, answer_1, answer_2) VALUES(?, ?, ?)', values)
        conn.commit()
        conn.close()

    def help_message(message):
        if message.text == '/help':
            bot.send_message(message.chat.id, 'Напишите старт для начала опроса')

    bot.polling(none_stop=True, interval=0)


main()
