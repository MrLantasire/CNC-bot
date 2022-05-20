from postprocessing import Postprocessor
from matrix import Matrix

class Cycle:

    @staticmethod
    def processing(data: tuple, file_name):
        heidenhain = Postprocessor(file_name)