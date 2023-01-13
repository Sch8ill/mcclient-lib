import socket
from mcclient.address import Address
from mcclient.encoding.packet import Packet
from mcclient.encoding.varint import VarInt



class BaseClient:
    def __init__(self, host="localhost", port=25565, timeout=5, version=47, srv=True):
        self.get_host(host, port, srv=srv)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.varint = VarInt()
        self.connected = False
        self.sock.settimeout(timeout)
        self.protocoll_version = self.varint.pack(version)


    def get_host(self, hostname, port, srv):
        addr = Address(hostname)
        addr = addr.get_host(srv)
        self.hostname = hostname
        self.host = addr[0]
        if addr[1] == None:
            self.port = port

        else:
            self.port = addr[1]


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
        packet_id = self.varint.pack(packet_id)
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
            self.hostname,
            25565,
            self.varint.pack(next_state)# next state 1 for status request
        )
        packet = Packet(fields)
        packet = packet.pack()
        self._send(packet)