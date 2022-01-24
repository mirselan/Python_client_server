"""Client-module"""

import socket
import sys
import time
import json
import argparse
import time

import logging
import log.client_log_config
from errors import ReqFieldMissingError, ServerError
from decos import log

from common.utils import *
from common.variables import *

# Логер клиента
cl_log = logging.getLogger('client')


@log
def server_side_message(message):
    # Обработчик сообщений других пользователей, поступающих с сервера
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        cl_log.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        cl_log.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def making_message(sock, account_name='Client'):
    # Запрашивает текст сообщения и возвращает его.

    user_message = input('Введите сообщение для отправки'
                         ' или \'#\' для завершения работы: ')
    if user_message == '#':
        sock.close()
        cl_log.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    user_mess_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: user_message
    }
    cl_log.debug(f'Сформирован словарь сообщения: {user_mess_dict}')
    return


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
    pars.add_argument('-m', '--mode', default='listen', nargs='?')
    names = pars.parse_args(sys.argv[1:])
    serv_address = names.addr
    serv_port = names.port
    client_mode = names.mode

    # Проверка номера порта
    if 1024 > serv_port > 65535:
        cl_log.critical(
            f'Попытка запуска клиента с некорректным номером порта: {serv_port}.'
            f'Номером порта может быть только число от 1024 до 65535.'
            f'Работа клиента завершается.')
        sys.exit(1)

    # Проверка режима работы клиента
    if client_mode not in ('listen', 'send'):
        cl_log.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return serv_address, serv_port, client_mode


def main():
    # Загрузка параметров коммандной строки
    serv_address, serv_port, client_mode = create_argument_parser()

    cl_log.info(f'Запущен клиент с параметрами: '
                f'адрес сервера: {serv_address}, порт: {serv_port},'
                f'режим работы: {client_mode}')

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
        sys.exit(1)
    except ServerError as error:
        cl_log.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as miss_error:
        cl_log.error(f'В ответе сервера отсутствует необходимое поле '
                     f'{miss_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        cl_log.critical(f'Не удалось подключиться к серверу'
                        f' {serv_address}:{serv_port}, '
                        f'удаленный компьютер отказал в запросе на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено,
        # начинаем обмен согласно установленному режиму.
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - 'отправка сообщений'
            if client_mode == 'send':
                try:
                    send_message(connection, making_message(connection))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    cl_log.error(f'Соединение с сервером '
                                 f'{serv_address} было потеряно.')
                    sys.exit(1)

            # Режим работы - 'приём сообщений':
            if client_mode == 'listen':
                try:
                    server_side_message(get_message(connection))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    cl_log.error(f'Соединение с сервером '
                                 f'{serv_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
