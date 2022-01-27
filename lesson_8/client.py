"""Client-module"""

import socket
import sys
import json
import argparse
import time

import logging
import log.client_log_config
from errors import ReqFieldMissingError, ServerError, IncorrectDataRecivedError
from decos import log
import threading

from common.utils import *
from common.variables import *

# Логер клиента
cl_log = logging.getLogger('client')


@log
def exit_message(account_name):
    # Создаёт словарь с сообщением о выходе
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def server_side_message(sock, my_username):
    # Обработчик сообщений других пользователей, поступающих с сервера
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                cl_log.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                            f'\n{message[MESSAGE_TEXT]}')
            else:
                cl_log.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            cl_log.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            cl_log.critical(f'Потеряно соединение с сервером.')
            break


@log
def making_message(sock, account_name='Client'):
    # Запрашивает текст сообщения и возвращает его.

    adressant = input('Введите получателя сообщения: ')
    user_message = input('Введите сообщение для отправки')
    user_mess_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        SENDER: account_name,
        DESTINATION: adressant,
        MESSAGE_TEXT: user_message
    }
    cl_log.debug(f'Сформирован словарь сообщения: {user_mess_dict}')
    try:
        send_message(sock, user_mess_dict)
        cl_log.info(f'Отправлено сообщение для пользователя {adressant}')
    except:
        cl_log.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    user_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            making_message(sock, username)
        elif command == 'help':
            user_help()
        elif command == 'exit':
            send_message(sock, exit_message(username))
            print('Завершение соединения.')
            cl_log.info('Завершение работы по команде пользователя.')
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@log
def making_presence(account_name):

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


def user_help():
    # Выводим справку по использованию
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def server_answer(message):
    # Разбор ответа сервера
    cl_log.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return f'The response is "200 : Ok"'
        elif message[RESPONSE] == 400:
            raise ServerError(f'The response is "400 : {message[ERROR]}"')
    raise ReqFieldMissingError(RESPONSE)


@log
def create_argument_parser():
    # Парсер аргументов коммандной строки

    pars = argparse.ArgumentParser()
    pars.add_argument('address', default=DEFAULT_IP, nargs='?')
    pars.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    pars.add_argument('-n', '--name', default=None, nargs='?')
    names = pars.parse_args(sys.argv[1:])
    serv_address = names.addr
    serv_port = names.port
    client_name = names.name

    # Проверка номера порта
    if 1024 > serv_port > 65535:
        cl_log.critical(
            f'Попытка запуска клиента с некорректным номером порта: {serv_port}.'
            f'Номером порта может быть только число от 1024 до 65535.'
            f'Работа клиента завершается.')
        sys.exit(1)
    return serv_address, serv_port, client_name


def main():
    # Сообщение о запуске
    print('Консольный месседжер. Клиентский модуль.')
    # Загрузка параметров коммандной строки
    serv_address, serv_port, client_name = create_argument_parser()
    # Проверяем, введено ли имя пользователя
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    cl_log.info(f'Запущен клиент с параметрами: '
                f'адрес сервера: {serv_address}, порт: {serv_port},'
                f'имя пользователя: {client_name}')

    # Инициализация сокета и обмен

    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((serv_address, serv_port))
        send_message(connection, making_presence(client_name))
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
        # Если соединение с сервером установлено корректно,
        # запускаем клиенский процесс приёма сообщний
        recv_proc = threading.Thread(target=server_side_message,
                                     args=(connection, client_name))
        recv_proc.daemon = True
        recv_proc.start()

        # Запускаем отправку сообщений и взаимодействие с пользователем.
        interface_proc = threading.Thread(target=user_interactive,
                                          args=(connection, client_name))
        interface_proc.daemon = True
        interface_proc.start()
        cl_log.debug('Запущены процессы')

        # Основной цикл
        while True:
            time.sleep(1)
            if recv_proc.is_alive() and interface_proc.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
