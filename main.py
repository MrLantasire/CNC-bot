from bot import Bot
from counter import Cycle
import config

TOKEN = config.telegram_token

class CNC:

    _range = (3, 3600)

    def __init__(self):
        self.__bot = Bot(TOKEN)
        self.__users = dict()
        self.__bot.callback((self.__handler))
        self.__bot.start()

    def __add_parameters(self, user_id, params):
        count_param = len(self.__users[user_id]['data'])
        error_flag = False
        for unit in params:
            if not error_flag and self.__is_number(unit):
                self.__users[user_id]['data'].append(float(unit))
                count_param += 1
                if count_param == 5 and not self.__is_out_of_range_digit(unit, *CNC._range):
                    self.__users[user_id]['data'].pop(count_param - 1)
                    error_flag = True
                    count_param -= 1
            else:
                error_flag = True
        self.__messages(user_id, count_param, error_flag)

    def __data(self, text: str, user_id):
        if not text.startswith('/'):
            if user_id in self.__users:
                elements = list()
                for par in text.replace('\n',',').replace(',,',',').split(','):
                    elements.append(par.strip())
                self.__add_parameters(user_id, elements)

    def __handler(self, text, user):
        if text == '/start':
            self.__say_hellow(user['id'], user['first_name'])
        elif text == '/probing':
            self.__probing(user['id'])
        else: 
            self.__data(text, user['id'])

    def __messages(self, user_id, num, error):
        if error:
            self.__bot.send_message(user_id, 'В ведённых Вами данных были найдены ошибки.' +
            '\nДля ввода допускаются только числа, а параметры должны разделяться запятой!')
        if num == 0:
            self.__bot.send_message(user_id, 'Введите приблизительную координату Х центра поверхности измерения:')
        elif num == 1:
            self.__bot.send_message(user_id, 'Введите приблизительную координату Y центра поверхности измерения:')
        elif num == 2:
            self.__bot.send_message(user_id, 'Введите координату Z высоты измерения:')
        elif num == 3:
            self.__bot.send_message(user_id, 'Введите приблизительный диаметр цилиндрической поверхности:')
        elif num == 4:
            if error:
                self.__bot.send_message(user_id, 'Допускаются целые числа от ' 
                + str(CNC._range[0]) + ' до ' + str(CNC._range[1]) + '!')
            self.__bot.send_message(user_id, 'Введите количество точек измерения:\nКоличество точек должно ' +
            'быть больше ' + str(CNC._range[0]) + ', но меньше ' + str(CNC._range[1]) + '!')
        elif num == 5:
            self.__bot.send_message(user_id, 'Введите начальный угол по оси C для измерения:')
        elif num == 6:
            self.__bot.send_message(user_id, 'Введите угловой шаг измерения:')
        else:
            self.__bot.send_message(user_id, 'Выполняю вычисления...')
            data = self.__users[user_id]['data']
            file_name = './programs/' + str(user_id) + '/' + 'probing.h'
            Cycle.processing(tuple(data), file_name)
            with open(file_name, 'rb') as reply:
                self.__bot.send_document(user_id, reply)
            self.__users.pop(user_id)

    def __probing(self, user_id):
        self.__users[user_id] = dict()
        self.__users[user_id]['data'] = list()
        self.__bot.send_message(user_id, 'Введите приблизительные координаты центра поверхности ' +
            'и высоту измерения (X, Y, Z). Параметры можно вводить через запятую или каждый на ' +
            'новой строке.')

    def __say_hellow(self, user_id, user_name):
        self.__bot.send_message(user_id, f'Привет, {user_name}!')
        self.__bot.send_message(user_id, 'Данный бот предназначен для формирования ' +
        'управляющей программы замера и поиска центра цилиндрической поверхности на ' +
        '5-осевом обрабатывающем центре со стойкой Heidenhain ' +
        'и кинематикой B+C с углом по оси B = 90 градусов. Для начала работы ' +
        'напечатайте или нажмите /probing .')

    @staticmethod
    def __is_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def __is_digit(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def __is_out_of_range_digit(string, min, max):
        if CNC.__is_digit(string):
            num = int(string)
            if min <= num <= max:
                return True
            else:
                return False
        else:
            return False

if __name__ == "__main__":
    test = CNC()
