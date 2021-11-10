"""Программа-клиент"""
import json
import sys
from contextlib import contextmanager
from socket import *

from common.utils import get_message, send_message
from common.variables import *
from log.client_log_config import *
from practice.common.do_dict_utils import do_presence, do_message, do_wait_message


@contextmanager
def socket_context(server_address, server_port, *args, **kw):
    s = socket(*args, **kw)
    s.connect((server_address, int(server_port)))
    try:
        yield s
    finally:
        s.close()


def user_message(sock):
    msg = ''
    while msg.strip() == '':
        msg = input('Ваше сообщение: ')
    msg = do_message(msg, sock)
    send_message(sock, msg)
    answer = ''
    try:
        resp = get_message(sock)
        answer = read_server_response(resp)
    except Exception as err:  # (ValueError, json.JSONDecodeError)
        CLIENT_LOG.error('Не удалось декодировать сообщение сервера.')
        print(err)
    if answer != '':
        return answer
    else:
        return CLIENT_LOG.error('Не удалось декодировать сообщение сервера.')


def user_connect(sock):
    user_name = input('Имя пользователя:\n')
    message_to_server = do_presence(sock, user_name.lower())
    send_message(sock, message_to_server)
    answer = ''
    try:
        answer = read_server_response(get_message(sock))
        CLIENT_LOG.info(answer)
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOG.error('Не удалось декодировать сообщение сервера.')
    if answer != '':
        return answer
    else:
        return CLIENT_LOG.error('Не удалось декодировать сообщение сервера.')


def user_wait_message(sock):
    message_to_server = do_wait_message(sock)
    send_message(sock, message_to_server)
    try:
        sock.settimeout(10)
        data = sock.recv(1024).decode('utf-8')

        return data
    except Exception:
        return 'Server not answered'


# @Log()
def read_server_response(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200 and MESSAGE in message:
            return {200: message[MESSAGE]}
        if message[RESPONSE] == 200:
            return {RESPONSE: 200}
        elif message[RESPONSE] == 409:
            return {409: 'User already connected'}
        return {RESPONSE: 400, ERROR: 'Bad Request'}
    raise ValueError


def main():
    """Загружаем параметры командной строки"""
    try:
        server_address = sys.argv[2]
        server_port = int(sys.argv[1])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOG.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        # print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    commands = {'connect',
                # 'авторизация',
                # 'отключение',
                # 'сообщение',
                # 'присоединиться',
                # 'отсоединиться',
                'message',
                'get', }
    user_input = input('Для выхода введите "quit"\nДля справки введите "help"\nКоманда:\n')
    # s = socket(AF_INET, SOCK_STREAM)
    # s.connect((server_address, server_port))
    while user_input.lower() != 'quit':

        # with socket_context(server_address, server_port, AF_INET, SOCK_STREAM) as s:
        if ((user_input.lower() not in commands) or (user_input.lower() == 'help')) and (user_input != ''):
            print(f'Доступные команды:')
            for item in commands:
                print(f'[{item}]')
            user_input = ''
        elif user_input == '':
            user_input = input('Команда:\n')
        if user_input.lower() in commands:
            if user_input.lower() == 'connect':
                with socket_context(server_address, server_port, AF_INET, SOCK_STREAM) as s:
                    print(user_connect(s))
            if user_input.lower() == 'get':
                with socket_context(server_address, server_port, AF_INET, SOCK_STREAM) as s:
                    try:
                        server_response = user_wait_message(s)
                        print(server_response)
                        print('Клиент переведен в режим приема сообщений')
                        while True:
                            s.settimeout(None)
                            data = s.recv(1024).decode('utf-8')
                            print(data)
                    except Exception as err:
                        print(err)
            if user_input.lower() == 'message':
                with socket_context(server_address, server_port, AF_INET, SOCK_STREAM) as s:
                    user_message(s)
            user_input = ''


if __name__ == '__main__':
    main()
