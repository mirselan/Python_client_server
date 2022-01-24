"""Client-unittest"""

import unittest
from common.variables import *
from client import making_presence, server_answer


class TestClient(unittest.TestCase):

    def test_making_presence(self):
        # Тест на корректный запрос
        test_data = making_presence()
        test_data[TIME] = 1.1  # Принудительная установка времени
        self.assertEqual(test_data, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Client'}})

    def test_200_ok(self):
        # Тест на корректный разбор кода 200
        self.assertEqual(server_answer({RESPONSE: 200}), 'The response is "200 : Ok"')

    def test_400_er(self):
        # Тест на корректный разбор кода 400
        self.assertEqual(server_answer({RESPONSE: 400, ERROR: 'Bad Request'}), 'The response is "400 : Bad Request"')


if __name__ == '__main__':
    unittest.main()
