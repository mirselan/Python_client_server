"""Server-unittest"""

import unittest
from common.variables import *
from server import message_from_client


class TestServer(unittest.TestCase):

    dict_200 = {RESPONSE: 200}
    dict_400 = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_wrong_act(self):
        # Неизвестное действие
        self.assertEqual(message_from_client(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Client'}}), self.dict_400)

    def test_not_act(self):
        # Нет действия
        self.assertEqual(message_from_client(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Client'}}), self.dict_400)

    def test_without_user(self):
        # Нет пользователя
        self.assertEqual(message_from_client(
            {ACTION: PRESENCE, TIME: '1.1'}), self.dict_400)

    def test_wrong_user(self):
        # Неизвестный пользователь
        self.assertEqual(message_from_client(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Client2'}}), self.dict_400)

    def test_200_ok(self):
        # Запрос без ошибок
        self.assertEqual(message_from_client(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Client'}}), self.dict_200)


if __name__ == '__main__':
    unittest.main()
