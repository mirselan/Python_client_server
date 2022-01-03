"""Client-module"""

import socket
import sys
import time

from common.utils import *
from common.variables import *


def making_presence(account_name='Client'):

    # Генерация запроса о присутствии клиента

    data = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return data


def server_answer(message):
    # Разбор ответа сервера

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'The response is "200 : Ok"'
        return f'The response is "400 : {message[ERROR]}"'
    raise ValueError


def main():
    # Загрузка параметров коммандной строки

    try:
        serv_address = sys.argv[1]
        serv_port = int(sys.argv[2])
        if 1024 > serv_port > 65535:
            raise ValueError
    except IndexError:
        serv_address, serv_port = DEFAULT_IP, DEFAULT_PORT
    except ValueError:
        print('Номером порта может быть только число от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((serv_address, serv_port))
    message_to_serv = making_presence()
    send_message(connection, message_to_serv)
    try:
        answer = server_answer(get_message(connection))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Сообщение от сервера декодировать не удалось.')


if __name__ == '__main__':
    main()
