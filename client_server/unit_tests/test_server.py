"""Unit-тесты сервера"""

import sys
import os
import unittest
import socket

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import *
from server import do_server_response
from common.utils import *
from client import *


class TestServer(unittest.TestCase):
    """
    В сервере только 1 функция для тестирования
    """
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(do_server_response(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

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

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(do_server_response(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_user_already_connected(self):
        """Ошибка - пользователь уже присоединился"""
        """Переменные сервера"""
        listen_address = ''
        listen_port = DEFAULT_PORT
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((listen_address, listen_port))
        server_socket.listen(MAX_CONNECTIONS)
        # client, client_address = server_socket.accept() https://stackoverflow.com/questions/5308080/python-socket-accept-nonblocking
        presences_users = {'Guest: ""'}
        """Переменные клиента"""
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        message_to_server = do_presence()
        send_message(client_socket, message_to_server)
        # if client_address[0] != "":
        message_from_client = get_message(client)
        response = do_server_response(message_from_client)
        send_message(client, response)
        self.assertEqual(read_server_response(get_message(client_socket)), self.ok_dict)
        client.close()
        client_socket.close()



if __name__ == '__main__':
    unittest.main()
