"""Логгер клиента - конфиг"""

import sys
import os
import logging
from common.variables import log_level
sys.path.append('../')

# Форматирование логов
cl_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Имя файла для логов
file_name = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(file_name, 'client.log')

# Создание обработчика для вывода сообщений с уровнем CRITICAL в поток stderr
str_handl = logging.StreamHandler(sys.stderr)
str_handl.setFormatter(cl_format)
str_handl.setLevel(logging.CRITICAL)

# Создание обработчика для вывода сообщений в файл

file_handl = logging.FileHandler(file_name, encoding='utf8')
file_handl.setFormatter(cl_format)

# Создание регистратора
logs = logging.getLogger('client')

# Добавление обработчиков в регистратор
logs.addHandler(str_handl)
logs.addHandler(file_handl)
logs.setLevel(log_level)

# Отладка
if __name__ == '__main__':
    logs.critical('Критическая ошибка')
    logs.error('Обнаружена ошибка')
    logs.debug('Отладка программы')
    logs.info('Информационное сообщение')
