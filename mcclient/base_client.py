import socket

from mcclient.address import Address
from mcclient.packet import OutboundPacket

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 25565
DEFAULT_TIMEOUT = 5
DEFAULT_PROTO = 47


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
        p = OutboundPacket(0)
        p.write_varint(self.protocol_version)
        p.write_string(self.address.get_host())
        p.write_ushort(self.address.get_port())
        p.write_varint(next_state)
        p.write(self.sock)

    def _close(self):
        self.sock.close()
        self.connected = False
