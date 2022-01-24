"""Server-module"""

import socket
import sys
import argparse
import json
import select
import time

import logging
import log.server_log_config
from errors import IncorrectDataRecivedError
from decos import log

from common.utils import *
from common.variables import *

# Логгер сервера.
serv_log = logging.getLogger('server')


@log
def message_from_client(message, messages_list, client):
    # Обрабатываем сообщение от клиента, возвращаем словарь с кодом ответа сервера
    serv_log.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Client':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def create_argument_parser():
    # Парсер аргументов коммандной строки

    pars = argparse.ArgumentParser()
    pars.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    pars.add_argument('-a', default='', nargs='?')
    names = pars.parse_args(sys.argv[1:])
    address = names.a
    port = names.p

    # проверка получения корретного номера порта для работы сервера.
    if 1024 > port > 65535:
        serv_log.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                          f'{port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return address, port


def main():

    # Загружаем параметры командной строки
    # ( значения по умоланию, если параметры отсутствуют).
    # Порт и адрес:
    port, address = create_argument_parser()

    serv_log.info(f'Сервер запущен, порт для подключений: {port}, '
                  f'адрес с которого принимаются подключения: {address}. '
                  f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Создаем сокет:

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((address, port))
    connection.settimeout(0.5)

    # список клиентов и сообщений
    clients_ls = []
    messages_ls = []

    # Слушаем порт:

    connection.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = connection.accept()
        except OSError:
            pass
        else:
            serv_log.info(f'Установлено соедение с компьютером {client_address}')
            clients_ls.append(client)
        recv_ls = []
        send_ls = []
        err_ls = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients_ls:
                recv_ls, send_ls, err_ls = select.select(clients_ls, clients_ls, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_ls:
            for client_with_message in recv_ls:
                try:
                    message_from_client(get_message(client_with_message),
                                        messages_ls, client_with_message)
                except:
                    serv_log.info(f'Клиент {client_with_message.getpeername()} '
                                  f'отключился от сервера.')
                    clients_ls.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages_ls and send_ls:
            message = {
                ACTION: MESSAGE,
                SENDER: messages_ls[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages_ls[0][1]
            }
            del messages_ls[0]
            for waiting_client in send_ls:
                try:
                    send_message(waiting_client, message)
                except:
                    serv_log.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients_ls.remove(waiting_client)


if __name__ == '__main__':
    main()

