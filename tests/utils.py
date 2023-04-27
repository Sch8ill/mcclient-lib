from unittest.mock import Mock

from mcclient.encoding.varint import VarInt


class TooManyPackets(Exception):
    def __init__(self, max_packets):
        message = f"Received too man packets (more than {max_packets})"
        super().__init__(message)


class BaseTestConn:
    varint = VarInt()

    def __init__(self):
        self.packets = 0
        self._buffer = b""

    def recv(self, length):
        data = self._buffer[:length]
        self._buffer = self._buffer[length:]
        return data

    def close(self):
        pass

    def respond(self, data):
        self._buffer += data


def create_mock_socket(mock_socket):
    socket = Mock()
    socket.socket = mock_socket
    return socket
