class Matrix:

    def __init__(self, data):
        self.__values = [[0]] 
        # Флаг транспонирования (1 - обычная, -1 - транспонированная)
        self.__istranspose = 1
        dim = Matrix.dimension(data)
        if len(dim) == 1:
            self.__create(1, dim[0], [data])
        elif len(dim) == 2:
            self.__create(dim[0], dim[1], data)
        else:
            raise TypeError('Ошибка размерности входных данных!')

    def __getitem__(self, pos: tuple):
        pos = pos[::self.__istranspose]
        return self.__values[pos[0]][pos[1]]

    def __create(self, row, colum, data):
        self.__values = [[0] * colum for i in range(row) ]
        for n, string in enumerate(data):
            if len(string) == self.size()[1]:
                for m, unit in enumerate(string):
                    self[n,m] = unit
            else:
                raise TypeError('Строки должны быть одной длины!')

    def __len__(self):
        return len(self.__values[0])*len(self.__values)

    def __setitem__(self, pos: tuple, value):
        pos = pos[::self.__istranspose]
        if isinstance(value, (float,int)):
            self.__values[pos[0]][pos[1]] = value
        else:
            raise TypeError('Неверный тип значения!')

    def __str__(self):
        if self.__istranspose > 0:
            return str(self.__values)
        else:
            return str(list(map(list, zip(*self.__values))))

    def size(self):
        return (len(self.__values), len(self.__values[0]))[::self.__istranspose]

    def transpose(self):
        self.__istranspose *= -1

    @staticmethod
    def dimension(obj):
        if isinstance(obj, (list,tuple)):
            out = list()
            out.append(len(obj))
            for unit in Matrix.dimension(obj[0]):
                out.append(unit)
            return tuple(out)
        else:
            return tuple()

    @staticmethod
    def identity(row, colum):
        return Matrix([ [(0 + int(i == j)) for i in range(colum)] for j in range(row)])
    
    @staticmethod
    def zero(row, colum):
        return Matrix([[0] * colum for i in range(row)])

a = [1,2,3]
test = Matrix(a)
test.transpose()
print(test)