"""Программа-сервер"""
import json
import select
import socket

from common.variables import *
from log.log import Log
from log.server_log_config import *

# Временное решение для хранения пользователей, не в файле, а в словаре
presences_users = {"guest": ''}


def read_requests(read_clients, all_clients):
    responses = dict()

    for sock in read_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            response = json.loads(data)
            responses[sock] = response
        except Exception as e:
            print(e)
            # print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
            sock.close()
            all_clients.remove(sock)

    return responses


def get_listen_socket(address):
    """Инициируем серверный сокет"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(MAX_CONNECTIONS)
    sock.settimeout(1)
    return sock


# @Log()
def prepare_server_response(message, all_clients, messages):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param all_clients:
    :param messages:
    :param message:
    :return:
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] not in presences_users:
        presences_users[message[USER][ACCOUNT_NAME]] = message[USER][STATUS]
        return {RESPONSE: 200}
    if ACTION in message and message[ACTION] == MSG:
        client_socket = str(message[FROM])
        messages[client_socket] = message[MESSAGE]
        return {RESPONSE: 200}
    if USER in message:
        if ACTION in message:
            if message[ACTION] == 'Wrong':
                return {RESPONSE: 400}
        if message[USER][ACCOUNT_NAME] in presences_users:
            return {RESPONSE: 409}
    return {RESPONSE: 400}


def do_server_responses(requests, clients_write, all_clients, messages):
    for sock in clients_write:
        if sock in requests:
            try:
                if requests[sock] == '':
                    raise Exception
                resp = prepare_server_response(requests[sock], all_clients, messages)
                js_message = json.dumps(resp)
                encoded_message = js_message.encode(DEFAULT_ENCODING)
                sock.send(encoded_message)
            except Exception as ex:
                # sock.fileno() - вернуть дескриптор файла сокетов (небольшое целое число)
                # sock.getpeername() - получить IP-адрес и номер порта клиента
                print(ex)
                print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
                sock.close()
                all_clients.remove(sock)


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

    all_clients = []
    messages = dict()
    server_address = (listen_address, listen_port)
    s = get_listen_socket(server_address)
    while True:
        try:
            client, client_address = s.accept()
        except OSError:
            pass
        else:
            print(f'Запрос от клиента с адресом {str(client_address)}')
            all_clients.append(client)
        finally:
            clients_write = []
            clients_read = []
            errors = []
            try:
                clients_read, clients_write, errors = select.select(all_clients, all_clients, errors, 0)
            except Exception as e:
                print(e)
                pass
            requests = dict()
            if clients_read:
                requests = read_requests(clients_read, all_clients)
            if all_clients:
                if messages:
                    for sock in all_clients:
                        for value in messages.values():
                            encoded_message = value.encode(DEFAULT_ENCODING)
                            sock.send(encoded_message)
            if requests:
                do_server_responses(requests, clients_write, all_clients, messages)
            # if messages:
            #     for key, value in messages.items():
            #         print(key, value)


if __name__ == '__main__':
    main()
