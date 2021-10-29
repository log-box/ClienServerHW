"""Программа-клиент"""

import json
import sys
import time
from socket import *

from common.utils import get_message, send_message
from common.variables import *


def do_authenticate(account_name, password):
    """
    Функция генерирует запрос об авторизации клиента (авторизация)
    :param account_name:
    :param password:
    :return:
    """
    out = {
        ACTION: AUTHENTICATE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD: password
        }
    }
    return out


def do_quit(account_name):
    """
    Функция отправляет запрос о выходе клиента (отключение)
    :param account_name:
    :return:
    """
    out = {
        ACTION: QUIT,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def do_presence(account_name='Guest', status='I`m online'):
    """
    Функция генерирует запрос о присутствии клиента (подключение)
    :param status:
    :param account_name:
    :return:
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: DEFAULT_PORT,
        TYPE: STATUS,
        USER: {
            ACCOUNT_NAME: account_name,
            STATUS: status
        }
    }
    return out


def do_message_to_user(to_user, message):
    """
    Функция генерирует сообщение пользователю или чату (Пользователь-Пользователь, Пользователь-Чат)
    :param message:
    :param to_user:
    :return:
    """
    out = {
        ACTION: MSG,
        TIME: time.time(),
        TO: to_user,
        FROM: ACCOUNT_NAME,  # Доделать через сохранение имени пользователя в файл(пока просто 'account_name')
        ENCODING: DEFAULT_ENCODING,
        MESSAGE: message
    }
    return out


def do_join_chat(room_name):
    """
    Функция Присоединяет пользователя к чату (Присоединиться к чату)
    :param room_name:
    :return:
    """
    out = {
        ACTION: JOIN,
        TIME: time.time(),
        ROOM: room_name
    }
    return out


def do_leave_chat(room_name):
    """
    Функция отсоединяет пользователя от чата (Покинуть чат)
    :param room_name:
    :return:
    """
    out = {
        ACTION: LEAVE,
        TIME: time.time(),
        ROOM: room_name
    }
    return out


def read_server_response(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return {RESPONSE: 200}
        elif message[RESPONSE] == 409:
            return {409: f'{message[ERROR]}'}
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
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    commands = {'подключение',
                'авторизация',
                'отключение',
                'сообщение',
                'присоединиться',
                'отсоединиться'}
    user_input = input('Для выхода введите "quit"\nДля справки введите "help"\nКоманда:\n')
    while user_input.lower() != 'quit':
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_address, server_port))
        if ((user_input.lower() not in commands) or (user_input.lower() == 'help')) and (user_input != ''):
            print(f'Доступные команды:')
            for item in commands:
                print(f'[{item}]')
            user_input = ''
        if user_input == '':
            user_input = input('Команда:\n')
        if user_input.lower() in commands:
            if user_input.lower() == 'подключение':
                user_name = input('Имя пользователя:\n')
                message_to_server = do_presence(user_name.lower())
                send_message(transport, message_to_server)
            user_input = ''
            try:
                answer = read_server_response(get_message(transport))
                print(answer)
            except (ValueError, json.JSONDecodeError):
                print('Не удалось декодировать сообщение сервера.')
            finally:
                transport.close()
        else:
            user_input = ''

if __name__ == '__main__':
    main()
