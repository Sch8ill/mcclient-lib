import socket
import struct

from mcclient.address import Address
from mcclient.encoding.packet import Packet
from mcclient.encoding.varint import pack_varint, read_varint

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 25565
DEFAULT_TIMEOUT = 5
DEFAULT_PROTO = 47


class IncompletePacket(Exception):
    def __init__(self, size, missing):
        super().__init__(f"Incomplete packet: missing {missing} from {size} bytes.")


class BaseClient:
    address: Address
    sock: socket.socket
    connected: bool
    protocol_version: int

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: int = DEFAULT_TIMEOUT,
                 proto: int = DEFAULT_PROTO, srv: bool = True) -> None:
        self.address = Address(host, port)
        self.connected = False
        self.protocol_version = proto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        if srv:
            self.address.resolve()

    def implant_socket(self, sock: socket.socket) -> None:
        self.sock = sock
        self.connected = True

    def _connect(self) -> None:
        if self.connected:
            return

        self.sock.connect(self.address.address())
        self.connected = True

    def _handshake(self, next_state: int = 1) -> None:
        packet = Packet(
            b"\x00",  # packet id
            pack_varint(self.protocol_version),
            self.address.get_host(),
            struct.pack(">H", self.address.get_port()),
            pack_varint(next_state)  # next state 1 for status request
        )
        self._send(packet)

    def _send(self, packet: Packet) -> int:
        return self.sock.send(packet.pack())

    def _recv(self) -> tuple[int, bytes]:
        length = read_varint(self.sock)
        packet_id = read_varint(self.sock)
        return packet_id, self._recv_bytes(length)

    def _recv_bytes(self, length: int) -> bytes:
        received = 0
        data = b""
        while received < length - len(pack_varint(length)):
            chunk = self.sock.recv(length - received)
            data += chunk
            received += len(chunk)

            if chunk == b"":
                raise IncompletePacket(length, length - received)

        return data

    def _close(self):
        self.sock.close()
        self.connected = False
