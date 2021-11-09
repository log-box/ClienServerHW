import time

from practice.common.variables import *


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


# @Log()
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


# @Log()
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


# @Log()
def do_message(message):
    """
    Функция генерирует сообщение пользователю или чату (Пользователь-Пользователь, Пользователь-Чат)
    :param message:
    :return:
    """
    out = {
        ACTION: MSG,
        TIME: time.time(),
        FROM: ACCOUNT_NAME,  # Доделать через сохранение имени пользователя в файл(пока просто 'account_name')
        ENCODING: DEFAULT_ENCODING,
        MESSAGE: message
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


# @Log()
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


# @Log()
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