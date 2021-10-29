"""Unit-тесты сервера"""

import os
import socket
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import do_server_response
from client import *


class TestServer(unittest.TestCase):
    """
    В сервере только 1 функция для тестирования
    """
    err_dict = {RESPONSE: 400}
    ok_dict = {RESPONSE: 200}
    user_already_connected_dict = {409: 'User already connected'}

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(do_server_response(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest', STATUS: 'I`m online'}}), self.ok_dict)

    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(do_server_response(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(do_server_response(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(do_server_response(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(do_server_response(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    # def test_unknown_user(self):
    #     """Ошибка - не Guest"""
    #     self.assertEqual(do_server_response(
    #         {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_user_already_connected(self):
        """Ошибка - пользователь уже присоединился"""
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        message_to_server = do_presence('Guest')
        send_message(client_socket, message_to_server)
        message_from_server = get_message(client_socket)
        message_from_server = read_server_response(message_from_server)
        self.assertEqual(message_from_server, self.user_already_connected_dict)
        client_socket.close()


if __name__ == '__main__':
    unittest.main()
