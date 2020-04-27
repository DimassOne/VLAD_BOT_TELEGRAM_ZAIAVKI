from keyss import tok
import telebot
from telebot import types
from pprint import pprint

bot = telebot.TeleBot(tok)



user_dict = dict()
class User(object):
    def __init__(self, city):
        self.citi = city

        keys = ['fullname','phone','driverSeria',
                'driverNumber','driverDate','car',
                'carModel','carColor','carNumber','carDate']
        for key in keys:
            self.key = None

# keys = ['fullname','phone','driverSeria',
#                 'driverNumber','driverDate','car',
#                 'carModel','carColor','carNumber','carDate']

@bot.message_handler(commands='[start],[help]')
def mess(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/about')
    btn2 = types.KeyboardButton('/reg')
    btn3 = types.KeyboardButton('/reg2')
    markup.add(btn1,btn2,btn3)
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Здравствуйте ' + message.from_user.first_name + ' что бы вы хотели узнать',
                     reply_markup=markup)
#
@bot.message_handler(commands='[/about]')
def mess(message):
    bot.send_message(message.chat.id, 'Мы надежная компания!')

@bot.message_handler(commands=['reg'])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Печора')
    btn2 = types.KeyboardButton('Вуктыл')
    btn3 = types.KeyboardButton('Ухта')
    btn4 = types.KeyboardButton('Сыктывкар')
    btn5 = types.KeyboardButton('Киров')
    markup.add(btn1,btn2,btn3,btn4,btn5)
    msg = bot.send_message(message.chat.id, 'Ваш город?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)
#
def process_city_step(message)->str:
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        markup = types.ReplyKeyboardRemove()
        msg = bot.send_message(chat_id, 'Введите вашу фамилию и имя', reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)
        pprint(user_dict[chat_id])
    except Exception as err:
        msg = bot.send_message(chat_id, 'Вы ввели что-то не то...')
        bot.register_next_step_handler(msg, process_city_step)
#
# def func(message, keys, string, onefunc, nextfunc, string2='Вы ввели что-то не то...'):
#     try:
#         chat_id = message.chat.id
#         user = user_dict[chat_id]
#         user.keys[0] = message.text
#         msg = bot.send_message(chat_id, string)
#         bot.register_next_step_handler(msg, nextfunc)
#     except Exception as err:
#         msg = bot.send_message(chat_id, string2)
#         bot.send_message(msg, onefunc)
#
#
def process_fullname_step(message):
    # func(message, keys, 'Введите номер телефона: ', process_fullname_step, process_phone_step)
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text
        msg = bot.send_message(chat_id, 'Введите номер телефона: ')
        bot.register_next_step_handler(msg, process_phone_step)
    except Exception as err:
        msg = bot.send_message(chat_id, 'Вы ввели что то не то...')
        bot.send_message(msg, process_fullname_step)
#
def process_phone_step(message):

    try:
        int(message.text)
        chat_id = message.chat.id

        user = user_dict[chat_id]
        user.phone = message.text
        msg = bot.send_message(chat_id, 'Серия водительского удостоверения')
        bot.register_next_step_handler(msg, process_driverSeria_step)
    except Exception as err:
        msg = bot.send_message(chat_id, 'Вы ввели что то не то...')
        bot.send_message(msg, process_phone_step)

def process_driverSeria_step(message):
    try:
        chat_id = message.chat.id

        user = user_dict[chat_id]
        user.driverSeria = message.text
        msg = bot.send_message(chat_id, 'Номер водительского удостоверения')
        bot.register_next_step_handler(msg, process_driverNumber_step)
        print(user.phone)
        print(user.fullname)
    except Exception as err:
        msg = bot.send_message(chat_id, 'Вы ввели что то не то...')
        bot.send_message(msg, process_driverSeria_step)

def process_driverNumber_step(message):
    try:
        chat_id = message.chat.id

        user = user_dict[chat_id]
        user.driverNumber = message.text
        msg = bot.send_message(chat_id, 'Выберите марку автомобиля')
        bot.register_next_step_handler(msg, process_carMarc_step)
        print(user.phone)
        print(user.fullname)
    except Exception as err:
        msg = bot.send_message(chat_id, 'Вы ввели что то не то...')
        bot.send_message(msg, process_driverSeria_step)

def process_carMarc_step(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.carModel = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Красная')
    btn2 = types.KeyboardButton('Вишневая')
    btn3 = types.KeyboardButton('Серая')
    markup.add(btn1,btn2,btn3)
    msg = bot.send_message(chat_id, 'Выберите цвет тачки ',reply_markup=markup)
    bot.register_next_step_handler(msg, exitsss)

def exitsss(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.carColor = message.text
    bot.send_message(chat_id, message.from_user.first_name + ' \n Ваши данные {}\n{}\n{}'.format(user.fullname, user.phone, user.driverNumber))

if __name__ == '__main__':
    bot.polling(none_stop=True)