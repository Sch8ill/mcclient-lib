import socket
import struct
from typing import Tuple


def pack(data: int) -> bytes:
    if data == 0:
        return b'\x00'

    ordinal = b''
    while data != 0:
        byte = data & 0x7F
        data >>= 7
        ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

    return ordinal


def read(sock: socket.socket) -> int:
    """
    Reads a Varint from a socket stream.

    Args:
        sock (socket.socket): The socket to read the Varint from.

    Returns:
        int: The decoded Varint value.
    """
    data, _ = _read_varint_from_stream(lambda: sock.recv(1)[0])
    return data


def unpack(data: bytes) -> Tuple[int, int]:
    """
    Unpacks a variable-length integer (Varint) from a byte sequence.

    Args:
        data (bytes): The byte sequence containing the Varint.

    Returns:
        tuple[int, int]: A tuple containing the unpacked Varint and the number of bytes consumed.
    """
    return _read_varint_from_stream(iter(data).__next__)


def _read_varint_from_stream(read_byte) -> Tuple[int, int]:
    value = 0
    size = 0

    for i in range(5):
        byte = read_byte()
        if byte is None:
            raise EOFError("Unexpected end of stream while reading Varint")

        value |= (byte & 0x7F) << 7 * i
        size += 1

        if not byte & 0x80:
            break

    return value, size
