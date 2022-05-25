from threading import Thread, Lock
import requests as rq
import types

class Bot:

  __url = 'https://api.telegram.org/bot'

  def __init__(self, token:str):
    self.__token = token
    self.__stop_flag = True
    self.__offset = 0
    self.polling = 20
    self.__callback = None
    self.__thread = Thread(target = self.__handler)
    self.__lock = Lock()
    self.__initialisation()

  @property
  def polling(self):
    return self.__polling

  @polling.setter
  def polling(self, timeout: int):
    if timeout > 0:
      self.__polling = timeout
    
  def __get_raw_response(self, offset : int = 0):
    request = Bot.__url + self.__token + '/getUpdates'
    data = dict()
    data['offset'] = offset
    data['timeout'] = self.polling
    out = rq.get(request, data=data, timeout = self.polling + 10)
    if out.status_code // 100 != 2:
      print('Ошибка запроса!')
      out = ''
    else:
      out = out.json()
      if out['ok']:
        out = out['result']
      else:
        out = ''
    return out

  def __handler(self):
    self.__lock.acquire()
    flag = self.__stop_flag
    self.__lock.release()
    while flag:
      data = self.__get_raw_response(self.__offset)
      for unit in data:
        if unit['update_id'] > self.__offset:
          self.__offset = unit['update_id']
          if 'message' in unit:
            if 'text' in unit['message']:
              self.__parse(unit['message'])
      self.__lock.acquire()
      flag = self.__stop_flag
      self.__lock.release()

  def __initialisation(self):
    data = self.__get_raw_response(-1)
    for unit in data:
      self.__offset = unit['update_id']

  def __parse(self, message):
      if message['text'] and self.__callback:
          self.__callback(message['text'], message['from'])

  # Метод для связи с фукнцией, вызываемой после ответа сервера
  def callback(self, func):
    if isinstance(func, (types.FunctionType, types.MethodType)):
      self.__callback = func

  def send_message(self, id, message : str):
    request = Bot.__url + self.__token + '/sendMessage'
    data = dict()
    data['chat_id'] = id
    data['text'] = message
    r = rq.post(request, data=data)
    if r.status_code // 100 != 2:
      print('Сообщение не доставлено!')
      return r.status_code

  def send_document(self, id, binary_file):
    request = Bot.__url + self.__token + '/sendDocument'
    data = dict()
    data['chat_id'] = id
    r = rq.post(request, data=data, files={'document': binary_file})
    if r.status_code // 100 != 2:
      print('Сообщение не доставлено!')
      return r.status_code

  def start(self):
    self.__lock.acquire()
    self.__stop_flag = True
    self.__lock.release()
    if not self.__thread.is_alive():
      self.__thread.start()

  def stop(self):
    self.__lock.acquire()
    self.__stop_flag = False
    self.__lock.release()
