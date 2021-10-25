"""Утилиты"""

import json
from socket import socket

from common.variables import MAX_PACKAGE_LENGTH, DEFAULT_ENCODING


def get_message(client):
    """
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    """
    client.settimeout(5.0)
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(DEFAULT_ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    else:
        raise ValueError


def send_message(_socket, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param _socket:
    :param message:
    :return:
    """
    if isinstance(_socket, socket):
        js_message = json.dumps(message)
        encoded_message = js_message.encode(DEFAULT_ENCODING)
        if isinstance(encoded_message, bytes):
            _socket.send(encoded_message)
        else:
            raise ValueError
    else:
        raise ValueError
