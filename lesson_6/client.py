"""Client-module"""

import socket
import sys
import time
import json
import argparse

import logging
import log.client_log_config
from errors import ReqFieldMissingError
from decos import log

from common.utils import *
from common.variables import *

# Логер клиента
cl_log = logging.getLogger('client')


@log
def making_presence(account_name='Client'):

    # Генерация запроса о присутствии клиента

    data = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    cl_log.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return data


@log
def server_answer(message):
    # Разбор ответа сервера
    cl_log.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'The response is "200 : Ok"'
        return f'The response is "400 : {message[ERROR]}"'
    raise ReqFieldMissingError(RESPONSE)


@log
def create_argument_parser():
    # Парсер аргументов коммандной строки

    pars = argparse.ArgumentParser()
    pars.add_argument('address', default=DEFAULT_IP, nargs='?')
    pars.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return pars


def main():
    # Загрузка параметров коммандной строки
    pars = create_argument_parser()
    names = pars.parse_args(sys.argv[1:])
    serv_address = names.address
    serv_port = names.port
    if 1024 > serv_port > 65535:
        cl_log.critical(
            f'Попытка запуска клиента с некорректным номером порта: {serv_port}.'
            f'Номером порта может быть только число от 1024 до 65535.'
            f'Работа клиента завершается.')
        sys.exit(1)

    cl_log.info(f'Запущен клиент с параметрами: '
                f'адрес сервера: {serv_address}, порт: {serv_port}')

    # Инициализация сокета и обмен

    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((serv_address, serv_port))
        message_to_serv = making_presence()
        send_message(connection, message_to_serv)
        answer = server_answer(get_message(connection))
        cl_log.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        cl_log.error('Сообщение от сервера декодировать не удалось.')
    except ReqFieldMissingError as miss_error:
        cl_log.error(f'В ответе сервера отсутствует необходимое поле '
                     f'{miss_error.missing_field}')
    except ConnectionRefusedError:
        cl_log.critical(f'Не удалось подключиться к серверу'
                        f' {serv_address}:{serv_port}, '
                        f'удаленный компьютер отказал в запросе на подключение.')


if __name__ == '__main__':
    main()
