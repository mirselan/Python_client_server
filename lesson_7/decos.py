"""Decorators"""

import sys

import logging
import log.client_log_config
import log.server_log_config

import traceback
import inspect

# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер
    logs = logging.getLogger('server')
else:
    # если не сервер, то клиент
    logs = logging.getLogger('client')


def log(func):
    # Функция-декоратор
    def log_save(*args, **kwargs):
        res = func(*args, **kwargs)
        logs.debug(f'Была вызвана функция {func.__name__}'
                   f' c параметрами {args}, {kwargs}. '
                   f'Вызов из модуля {func.__module__}. Вызов из функции'
                   f' {traceback.format_stack()[0].strip().split()[-1]}.'
                   f'Вызов из функции {inspect.stack()[1][3]}')
        return res
    return log_save

