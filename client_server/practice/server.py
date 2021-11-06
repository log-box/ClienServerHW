"""Программа-сервер"""

import socket
import sys
import json

from common.variables import *
from common.utils import get_message, send_message
from log.log import Log
from log.server_log_config import *
# Временное решение для хранения пользователей, не в файле, а в словаре
presences_users = {"guest": ''}


def check_user_connection():
    pass

@Log()
def do_server_response(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] not in presences_users:
        presences_users[message[USER][ACCOUNT_NAME]] = message[USER][STATUS]
        return {RESPONSE: 200}
    if USER in message:
        if ACTION in message:
            if message[ACTION] == 'Wrong':
                return {RESPONSE: 400}
        if message[USER][ACCOUNT_NAME] in presences_users:
            return {RESPONSE: 409}
    return {RESPONSE: 400}


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            # DEFAULT_PORT = listen_port
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOG.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOG.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        SERVER_LOG.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    SERVER_LOG.info(f'Server started on port {listen_port}')
    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        if client_address[0] != "":
            try:
                message_from_client = get_message(client)
                SERVER_LOG.info(message_from_client)
                response = do_server_response(message_from_client)
                send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                SERVER_LOG.error(f'Принято некорретное сообщение от клиента: {message_from_client}')
                client.close()


if __name__ == '__main__':
    main()
