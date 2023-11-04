'''
Идея программы.
* Поступает запрос на местоположение определенного человека. Этому человеку (по его id) скидывает сообщение.
* Человек отправляет свои координаты. При отправлении координат записываются в БД широта и долгота.
* Запрашиваемому скидываются координаты посредством bot.send_location(message.chat.id, *latitude*, *longitude*)
'''

import telebot
from telebot import types

bot = telebot.TeleBot('6447415648:AAHAZrEnHgt7Vtlq8aaptxLuGUd4ZlQCLig')

'''
* Запрос. В вашу строку в БД вставляется id человека, которому необходимо ваше местоположение
* Постоянная проверка собственной строки. Если стобец с id вызвавшего запрос человека
не равен нулю, то отправить себе сообщение с предложением отправить ему координаты
* Отправка собственной геолокации по известному id
* Зануление строки с id вызвавшему запрос человека   
'''
senderID = ''

@bot.message_handler(commands=["start"])
def registration(message):
    # Внести в базу данных основные сведения о человеке, который только включил бота
    bot.send_message(message.chat.id, 'ФИО?')
    # Создание кнопки
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить местоположение", request_location=True))

@bot.message_handler(content_types=["location"])
def send(message):
    # Отправка по id
    global senderID
    if senderID != '':
        bot.send_message(senderID, f'Пользователь {message.from_user.id} находится здесь:')
        bot.send_location(senderID, message.location.latitude, message.location.longitude)
        # Если я отправлю при запросе от меня же, то мне придет моя геолокация
        # Поэтому необходимо занулить эту строку
        senderID = ''

@bot.message_handler(commands=["find"])
def find(message):
    # Просьба указать интересуемого коллегу
    bot.send_message(message.chat.id, 'Напишите id человека, которого вы хотите найти') # Запрос должен быть по имени/должности!
    # Отправить ему уведомление
    bot.register_next_step_handler(message, notification)

def notification(message):
    global senderID
    senderID = message.from_user.id
    bot.send_message(senderID, 'Уведомление отправлено!')
    bot.send_message(message.text, f'Пользователь {senderID} хочет знать ваше местоположение')

bot.polling(non_stop=True)