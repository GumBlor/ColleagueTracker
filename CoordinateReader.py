import telebot
from telebot import types

bot = telebot.TeleBot('6447415648:AAHAZrEnHgt7Vtlq8aaptxLuGUd4ZlQCLig')

senderID = ''

@bot.message_handler(commands=["start"])
def start(message):
    # Создание кнопки
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить местоположение", request_location=True))
    # Регистрация
    registration(message)

@bot.message_handler(commands=["registration"])
def registration(message):
    # Внести в базу данных основные сведения о человеке
    bot.send_message(message.chat.id, 'Введите вашу фамилию')
    '''
        Создание строки с двумя столбцами:
            * message.text (фамилия)
            * message.from_user.id (id пользователя)
    '''

@bot.message_handler(content_types=["location"])
def send(message):
    # Отправка по id
    global senderID
    if senderID != '':
        bot.send_message(senderID, f'Пользователь {message.from_user.id} находится здесь:')
        bot.send_location(senderID, message.location.latitude, message.location.longitude)
        # Если я отправлю при запросе от меня же, то мне придет моя геолокация
        # Поэтому необходимо занулить эту строку:
        senderID = ''

@bot.message_handler(commands=["find"])
def find(message):
    # Просьба указать интересуемого коллегу
    bot.send_message(message.chat.id, 'Напишите id человека, которого вы хотите найти')
    '''
        Здесь необходимо запросить местоположение по фамилии, по ней находится строка в базе данных.
        В соседнем столбце находится id человека
    '''
    # Отправить ему уведомление
    bot.register_next_step_handler(message, notification)

def notification(message):
    global senderID
    senderID = message.from_user.id
    bot.send_message(senderID, 'Уведомление отправлено!')
    bot.send_message(message.text, f'Пользователь {senderID} хочет знать ваше местоположение')

bot.polling(non_stop=True)