"""Логгер сервера - конфиг"""

import sys
import os
#import logging
import logging.handlers
from common.variables import log_level
sys.path.append('../')

# Форматирование логов
serv_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Имя файла для логов
file_name = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(file_name, 'server.log')

# Создание обработчика для вывода сообщений с уровнем CRITICAL в поток stderr
str_handl = logging.StreamHandler(sys.stderr)
str_handl.setFormatter(serv_format)
str_handl.setLevel(logging.CRITICAL)

# Создание обработчика для вывода сообщений в файл
# с ежедневной ротацией лог-файлов в полночь

file_handl = logging.handlers.TimedRotatingFileHandler(file_name, encoding='utf8', interval=1, when='midnight')
file_handl.setFormatter(serv_format)

# Создание регистратора
logs = logging.getLogger('server')

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
