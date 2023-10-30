'''
* Команда start - начинается считывание координат и дальнейшая передача серверу
* Команда end - считывание координат заканчивается
'''

import telebot
from telebot import types

bot = telebot.TeleBot('6447415648:AAHAZrEnHgt7Vtlq8aaptxLuGUd4ZlQCLig')

@bot.message_handler(commands=["start"])
def main(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить местоположение", request_location=True))
    bot.send_message(message.chat.id, "Отправьте свои коордианты!", reply_markup=keyboard)

    bot.register_next_step_handler(message, click)

def click(message):
    bot.send_message(message.chat.id, f'latitude: {message.location.latitude}, longitude: {message.location.longitude}')

    #Команда, которая отправляет карту по заданным координатам:
    #bot.send_location(message.chat.id, 1.1, 10)

bot.polling(non_stop=True)