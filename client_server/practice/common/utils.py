"""Утилиты"""

import json
from socket import socket

from common.variables import MAX_PACKAGE_LENGTH, DEFAULT_ENCODING
from errors import IncorrectDataRecivedError, NonDictInputError
from log.log import Log


@Log()
def get_message(_socket):
    encoded_response = _socket.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(DEFAULT_ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise IncorrectDataRecivedError
    else:
        raise IncorrectDataRecivedError


@Log()
def send_message(_socket, message):
    if isinstance(_socket, socket):
        js_message = json.dumps(message)
        encoded_message = js_message.encode(DEFAULT_ENCODING)
        if isinstance(encoded_message, bytes):
            _socket.send(encoded_message)
        else:
            raise NonDictInputError
    else:
        raise NonDictInputError



