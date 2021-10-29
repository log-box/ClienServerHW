"""Unit-тесты клиента"""

import os
import sys
import unittest

# sys.path.append(os.path.join(os.getcwd(), '..'))
from client import *


class TestClass(unittest.TestCase):
    '''
    Класс с тестами
    '''

    def test_def_presense(self):
        """Тест коректного запроса"""
        test = do_presence()
        test[TIME] = 1.1  # время необходимо приравнять принудительно
        # иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, PORT: DEFAULT_PORT, TYPE: STATUS,
                                USER: {ACCOUNT_NAME: 'Guest', STATUS: 'I`m online'}})

    def test_200_ans(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(read_server_response({RESPONSE: 200}), {RESPONSE: 200})

    def test_400_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(read_server_response({RESPONSE: 400, ERROR: 'Bad Request'}),
                         {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, read_server_response, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
