import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6447415648:AAHAZrEnHgt7Vtlq8aaptxLuGUd4ZlQCLig')

senderID = ''

@bot.message_handler(commands=["start"])
def start(message):
    # Создание кнопки
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить местоположение", request_location=True))
    # Создание базы данных
    conn = sqlite3.connect('Data.dat')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(50), userID varchar(9))')
    conn.commit()
    cur.close()
    conn.close()
    # Регистрация
    registration(message)

@bot.message_handler(commands=["registration"])
def registration(message):
    bot.send_message(message.chat.id, 'Введите ваше имя')
    # Вывести поздравление
    bot.register_next_step_handler(message, congratulations)

def congratulations(message):
    # Добавление в базу данных имени и id пользователя
    conn = sqlite3.connect('Data.dat')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, userID) VALUES ('%s', '%s')" % (message.text.upper(), message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()
    # Поздравление
    bot.send_message(message.chat.id, f'Приятно познакомиться, {message.text}!')

@bot.message_handler(content_types=["location"])
def send(message):
    global senderID
    if senderID != '':
        # Найти имя пользователя по id
        conn = sqlite3.connect('Data.dat')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        for user in users:
            if str(user[1]) == str(message.from_user.id):
                bot.send_message(senderID, f'{user[0]} находится здесь')

        cur.close()
        conn.close()

        # Отправить живую карту
        bot.send_location(senderID, message.location.latitude, message.location.longitude, live_period=900)
        # Если я отправлю при запросе от меня же, то мне придет моя геолокация
        # Поэтому необходимо занулить эту строку:
        senderID = ''

@bot.message_handler(commands=["find"])
def find(message):
    # Просьба указать интересуемого коллегу
    bot.send_message(message.chat.id, 'Напишите имя человека, которого вы хотите найти')
    # Отправить ему уведомление
    bot.register_next_step_handler(message, notification)

def notification(message):
    global senderID
    senderID = message.from_user.id
    wantedID = ''

    # Найти id пользователя по имени и имя пользователя по id
    conn = sqlite3.connect('Data.dat')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    for user in users:
        if user[0] == message.text.upper():
            wantedID = user[1]
        if str(user[1]) == str(senderID):
            bot.send_message(wantedID, f'{user[0]} хочет знать ваше местоположение')

    cur.close()
    conn.close()

    # Рассылка
    bot.send_message(senderID, 'Уведомление отправлено!')

bot.polling(non_stop=True)