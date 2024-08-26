import socket
import struct

from mcclient.packet.varint import pack


class OutboundPacket:
    """
    Represents an outbound packet that can be sent over a socket.
    """

    def __init__(self, packet_id: int):
        """
        Initializes the OutboundPacket with the specified packet ID.

        Args:
            packet_id (int): The packet ID representing the type of packet.
        """
        self.id = packet_id
        self.data = b""

    def write_int(self, value: int) -> None:
        """
        Writes a 4-byte integer to the packet.

        Args:
            value (int): The integer value to write.
        """
        self.data += struct.pack('>i', value)

    def write_short(self, value: int) -> None:
        """
        Writes a 2-byte short integer to the packet.

        Args:
            value (int): The short integer value to write.
        """
        self.data += struct.pack('>h', value)

    def write_ushort(self, value: int) -> None:
        """
        Writes a 2-byte unsigned short integer to the packet.

        Args:
            value (int): The unsigned short integer value to write.
        """
        self.data += struct.pack('>H', value)

    def write_long(self, value: int) -> None:
        """
        Writes an 8-byte long integer to the packet.

        Args:
            value (int): The long integer value to write.
        """
        self.data += struct.pack('>q', value)

    def write_varint(self, varint: int) -> None:
        """
        Writes a variable-length integer (VarInt) to the packet.

        Args:
            varint (int): The VarInt value to write.
        """
        self.data += pack(varint)

    def write_bool(self, value: bool) -> None:
        """
        Writes a boolean value to the packet as a single byte.

        Args:
            value (bool): The boolean value to write. True is represented
                          as 0x01, and False as 0x00.
        """
        self.data += b"\x01" if value else b"\x00"

    def write_string(self, string: str) -> None:
        """
        Writes a UTF-8 encoded string to the packet.

        Args:
            string (str): The string to write.
        """
        self.write_varint(len(string))
        self.data += string.encode('utf-8')

    def write_bytes(self, data: bytes) -> None:
        """
        Writes raw bytes directly to the packet.

        Args:
            data (bytes): The bytes to write.
        """
        self.data += data

    def pack(self) -> bytes:
        """
        Packs the packet data, including the packet ID and length, into a
        single byte sequence.

        Returns:
            bytes: The packed packet ready for transmission.
        """
        data = pack(self.id) + self.data
        return pack(len(data)) + data

    def write(self, sock: socket.socket) -> None:
        """
        Sends the packet over the specified socket.

        This method packs the packet, including the packet ID and length,
        and then sends it to the remote socket.

        Args:
            sock (socket.socket): The socket to send the packet over.
        """
        sock.send(self.pack())
