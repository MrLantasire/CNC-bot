from math import sin, cos, pi

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
            raise ValueError('Ошибка размерности входных данных!')

    def __add__(self, second):
        if isinstance(second, Matrix):
            size = self.size()
            if size == second.size():
                out = [[self[i,j] + second[i,j] for j in range(size[1])] for i in range(size[0])]
                return Matrix(out)
            else:
                raise ValueError('Матрицы разного размера!')
        else:
            raise TypeError('Второе слагаемое не является матрицей!')

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
                raise ValueError('Строки должны быть одной длины!')

    def __len__(self):
        return len(self.__values[0])*len(self.__values)

    def __mul__(self, second):
        size = self.size()
        if isinstance(second, (float, int)):
            out = [[self[i,j] * second for j in range(size[1])] for i in range(size[0])]
            return Matrix(out)
        elif isinstance(second, Matrix):
            if size[1] == second.size()[0]: 
                return Matrix(self.__multiply(second))
            else:
                raise ValueError('Количество столбцов первой матрицы не равно количеству строко второй!')
        else:
            raise TypeError('Умножение с данным типом данных не поддерживается!')

    def __multiply(self, matrix):
        out = list()
        f_size = self.size()
        s_size = matrix.size()
        for n in range(f_size[0]):
            out.append(list())
            for m in range(s_size[1]):
                out[n].append(0)
                for i in range(f_size[1]):
                    out[n][m] += self[n,i]*matrix[i,m]
        return out

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
        return self

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
    def length(vector):
        out = 0
        for unit in vector:
            out += unit ** 2
        return out ** (1/2)

    @staticmethod
    def normalize(vector):
        length = Matrix.length(vector)
        out = list()
        for unit in vector:
            if length:
                out.append(unit/length)
            else:
                out.append(unit)
        return out

    @staticmethod
    def transformation3D(vector, angle):
        u = Matrix.normalize(vector)
        grad = (angle * pi)/180. 
        return Matrix([
            [ ( u[0]*u[0] + cos(grad)*(1-u[0]*u[0]) ),
              ( u[0]*u[1]*(1-cos(grad)) - u[2]*sin(grad) ),
              ( u[2]*u[0]*(1-cos(grad)) + u[1]*sin(grad) )],
            [ ( u[0]*u[1]*(1-cos(grad)) + u[2]*sin(grad) ),
              ( u[1]*u[1] + cos(grad)*(1-u[1]*u[1]) ),
              ( u[1]*u[2]*(1-cos(grad)) - u[0]*sin(grad) )],
            [ ( u[2]*u[0]*(1-cos(grad)) - u[1]*sin(grad) ),
              ( u[1]*u[2]*(1-cos(grad)) + u[0]*sin(grad) ),
              ( u[2]*u[2] + cos(grad)*(1-u[2]*u[2]) )] ])

    @staticmethod
    def zero(row, colum):
        return Matrix([[0] * colum for i in range(row)])
