"""Utils"""

import json
from common.variables import MAX_MESSAGE_LENGTH, ENCODING


def get_message(guest):

    # Утилита приёма и декодирования сообщений

    get_response = guest.recv(MAX_MESSAGE_LENGTH)
    if isinstance(get_response, bytes):
        js_response = get_response.decode(ENCODING)
        final_response = json.loads(js_response)
        if isinstance(final_response, dict):
            return final_response
        raise ValueError
    raise ValueError


def send_message(sock, message):

    # Утилита кодирования и отправки сообщений

    js_message = json.dumps(message)
    sent_message_to = js_message.encode(ENCODING)
    sock.send(sent_message_to)
