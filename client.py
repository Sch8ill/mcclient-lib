
__version__ = "0.2.8"
__author__ = "Sch8ill"


import socket
from utils import Packet, VarInt



class MCClient:
    def __init__(self, host="localhost", port=25565, timeout=5, version=47):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.varint = VarInt()
        self.connected = False
        self.retries = 0
        self.sock.settimeout(timeout)
        self.protocoll_version = self.varint.pack(version)


    def _connect(self):
        if self.connected == False:
            self.sock.connect((self.host, self.port))
            self.connected = True

        elif self.connected == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connected = False
            self._connect()


    def _send(self, packet):
        return self.sock.send(packet)

    
    def _recv(self):
        length = self.varint.unpack(self.sock)
        packet_id = self.varint.unpack(self.sock)
        data = self.sock.recv(length)
        if len(data) < length - 4:
            loss = True
        
        else:
            loss = False
        return loss, packet_id, data


    def _close(self, flush=True):
        if flush:
            self._flush()
        self.sock.close()
        self.connected = None


    def _reset(self):
        self._close()
        self._connect()
        self._handshake()


    def _flush(self, length=8192):
        self.sock.recv(length)


    def _handshake(self, next_state=1):
        fields = (
            b"\x00", # packet id
            self.protocoll_version,
            self.host,
            25565,
            self.varint.pack(next_state)# next state 1 for status request
        )
        packet = Packet(fields)
        packet = packet.pack()
        self._send(packet)