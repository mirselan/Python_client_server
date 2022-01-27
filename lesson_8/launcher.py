"""Launcher-module"""

import subprocess

p_list = []

while True:
    user_action = input('Выберите действие: q - выход, '
                        's - запустить сервер и клиенты, '
                        'x - закрыть все окна: ')

    if user_action == 'q':
        break
    elif user_action == 's':
        p_list.append(subprocess.Popen(
            'python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            p_list.append(subprocess.Popen(
                'python client.py -m send',
                creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            p_list.append(subprocess.Popen(
                'python client.py -m listen',
                creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif user_action == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()

