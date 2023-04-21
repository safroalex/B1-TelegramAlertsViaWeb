import telebot
from telebot import types
import sqlite3

from config import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)
name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment\
                 primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем!\
 Введи твое имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    name = message.text.strip()  # noqa: F841
    bot.send_message(message.chat.id, 'ВВедите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')"
                % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей',
                                                  callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!',
                                      reply_markup=markup)


bot.polling(none_stop=True)
