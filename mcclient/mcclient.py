
__author__ = "Sch8ill"


import time
import socket
from mcclient.base_client import BaseClient
from mcclient.encoding.varint import VarInt
from mcclient.encoding.packet import Packet


class MCClient(BaseClient):
    def __init__(self, host="localhost", port=25565, timeout=5, version=760):
        super().__init__(host=host, port=port, timeout=timeout, version=version)


    def connect(self):
        self._connect()
        self._handshake(next_state=2)

    def login(self, player):
        self._login_start(player)


    def _login_start(self, player): # https://wiki.vg/Protocol#Login
        fields = (
            b"\x00", # packet id
            player.name,
            False,
            False
        )
        packet = Packet(fields)
        packet = packet.pack()
        self._send(packet)
        print(self._recv())
        time.sleep(1)
        print(self._recv())