from bot import Bot
from postprocessing import Postprocessor
from matrix import Matrix
import config

TOKEN = config.telegram_token

class CNC:

    def __init__(self):
        self.__bot = Bot(TOKEN)
        self.__users = dict()
        self.__bot.callback((self.__handler))
        self.__bot.start()

    def __data(self, user_id):
        pass

    def __handler(self, text, user):
        if text == '/start':
            self.__say_hellow(user['id'], user['first_name'])
        elif text == '/probing':
            self.__probing(user['id'])
        else: 
            self.__data(user['id'])

    def __probing(self, user_id):
        self.__users[user_id] = dict()
        self.__users[user_id]['data'] = list()
        self.__users[user_id]['step'] = 0
        self.__bot.send_message(user_id, 'Введите приблизительные координаты центра поверхности \
            и высоту измерения (X, Y, Z).')

    def __say_hellow(self, user_id, user_name):
        self.__bot.send_message(user_id, f'Привет, {user_name}!')
        self.__bot.send_message(user_id, 'Данный бот предназначен для формирования \
        управляющей программы замера и поиска центра цилиндрической поверхности на \
        5-осевом обрабатывающем центре со стойкой Heidenhain \
        и кинематикой B+C с углом по оси B = 90 градусов. Для начала работы \
        напечатайте или нажмите /probing .')

test = CNC()
