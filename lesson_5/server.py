"""Server-module"""

import socket
import sys
import argparse
import json

import logging
import log.server_log_config
from errors import IncorrectDataRecivedError

from common.utils import *
from common.variables import *

# Логгер сервера.
serv_log = logging.getLogger('server')


def message_from_client(message):
    # Обрабатываем сообщение от клиента, возвращаем словарь с кодом ответа сервера
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Client':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def create_argument_parser():
    # Парсер аргументов коммандной строки

    pars = argparse.ArgumentParser()
    pars.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    pars.add_argument('-a', default='', nargs='?')
    return pars


def main():

    # Загружаем параметры командной строки
    # ( значения по умоланию, если параметры отсутствуют).
    # Порт и адрес:
    pars = create_argument_parser()
    names = pars.parse_args(sys.argv[1:])
    address = names.a
    port = names.p
    if 1024 > port > 65535:
        serv_log.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                          f'{port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    serv_log.info(f'Сервер запущен, порт для подключений: {port}, '
                  f'адрес с которого принимаются подключения: {address}. '
                  f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Создаем сокет:

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((address, port))

    # Слушаем порт:

    connection.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = connection.accept()
        serv_log.info(f'Установлено соедение с компьютером {client_address}')
        try:
            client_message = get_message(client)
            serv_log.debug(f'Получено сообщение {client_message}')
            response = message_from_client(client_message)
            serv_log.info(f'Готов ответ клиенту {response}')
            send_message(client, response)
            serv_log.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            serv_log.error(f'Не удалось декодировать сообщение от клиента'
                           f' {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            serv_log.error(f'От клиента {client_address} приняты '
                           f'некорректные данные. Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
