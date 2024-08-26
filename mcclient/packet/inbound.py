import socket
import struct

from mcclient.packet.varint import read, pack, unpack


class IncompletePacket(Exception):
    def __init__(self, size, missing):
        super().__init__(f"Incomplete packet: missing {missing} from {size} bytes.")


class InboundPacket:
    """
    Represents an inbound packet received from a socket.
    """

    def __init__(self, sock: socket.socket):
        """
        Initializes the InboundPacket by receiving data from a socket.

        Args:
            sock (socket.socket): The socket from which the packet is received.
        """

        self.sock = sock
        self.length = read(self.sock)
        self.id = read(self.sock)
        id_size = len(pack(self.id))

        remaining = self.length - id_size
        self.data = b""
        while len(self.data) < remaining:
            chunk = self.sock.recv(remaining - len(self.data))
            if chunk == b"":
                packet_size = len(pack(self.length)) + id_size + self.length
                raise IncompletePacket(packet_size, self.length - id_size - len(self.data))

            self.data += chunk

    def read_int(self) -> int:
        """
        Reads a 4-byte integer from the data.

        Returns:
            int: The read integer value.
        """
        return struct.unpack('>i', self.read_bytes(4))[0]

    def read_short(self) -> int:
        """
        Reads a 2-byte short integer from the data.

        Returns:
            int: The read short integer value.
        """
        return struct.unpack('>h', self.read_bytes(2))[0]

    def read_ushort(self) -> int:
        """
        Reads a 2-byte unsigned short integer from the data.

        Returns:
            int: The read unsigned short integer value.
        """
        return struct.unpack('>H', self.read_bytes(2))[0]

    def read_long(self) -> int:
        """
        Reads an 8-byte long integer from the data.

        Returns:
            int: The read long integer value.
        """
        return struct.unpack('>q', self.read_bytes(8))[0]

    def read_varint(self) -> int:
        """
        Reads a variable-length integer (Varint) from the data.

        Returns:
            int: The read Varint value.
        """
        varint, size = unpack(self.data)
        self.read_bytes(size)
        return varint

    def read_bool(self) -> bool:
        """
        Reads a boolean value from the data.

        Returns:
            bool: The read boolean value.
        """
        value = self.data[0] == 1
        self.data = self.data[1:]
        return value

    def read_string(self) -> str:
        """
        Reads a string from the data.

        Returns:
            str: The read string.
        """
        length = self.read_varint()
        string = self.data[:length].decode('utf-8')
        self.data = self.data[length:]
        return string

    def read_bytes(self, length: int) -> bytes:
        """
        Reads a specified number of bytes from the data.

        Args:
            length (int): The number of bytes to read.

        Returns:
            bytes: The read bytes.
        """
        bytes_data = self.data[:length]
        self.data = self.data[length:]
        return bytes_data
