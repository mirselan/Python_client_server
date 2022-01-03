"""Server-module"""

import socket
import sys

from common.utils import *
from common.variables import *


def message_from_client(message):
    # Обрабатываем сообщение от клиента, возвращаем словарь с кодом ответа сервера
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Client':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():

    # Загружаем параметры командной строки( значения по умоланию, если параметры отсутствуют).
    # Порт:
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if 1024 > port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' укажите номер порта.')
        sys.exit(1)
    except ValueError:
        print('Номером порта может быть только число от 1024 до 65535.')
        sys.exit(1)

    # Адрес, который слушает сервер:

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = ''

    except IndexError:
        print('После параметра \'a\'- укажите адрес, который нужно слушать серверу.')
        sys.exit(1)

    # Создаем сокет:

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((address, port))

    # Слушаем порт:

    connection.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = connection.accept()
        try:
            client_message = get_message(client)
            print(client_message)
            response = message_from_client(client_message)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорректный запрос от клиента.')
            client.close()


if __name__ == '__main__':
    main()
