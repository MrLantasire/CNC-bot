import os

class Postprocessor:

    def __init__(self, full_file_name: str):
        self.__filename = full_file_name
        # Счетчик кадров
        self.__line = 0
        # Создание файла
        path, file = os.path.split(self.__filename)
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(self.__filename, 'w+')
        file.close()

    def write_line(self, *text, withnumber: bool = True, sep : str = ' ', end : str = '\n' ):
        out = list()
        if withnumber:
            out.append(str(self.__line))
            self.__line += 1
        for word in text:
            out.append(str(word))
        out.append(end)
        out = sep.join(out)
        with open(self.__filename, 'a+') as file:
            file.write(out)