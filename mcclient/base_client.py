
__author__ = "Sch8ill"

import struct
import socket
from mcclient.encoding.packet import Packet
from mcclient.encoding.varint import VarInt

class VarInt: # class to pack and unpack Varints
    @staticmethod
    def pack(data):
        ordinal = b''
        while data != 0:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))
        return ordinal


    @staticmethod
    def unpack(sock):
        data = 0
        for i in range(5):
            ordinal = sock.recv(1)
            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7*i
            if not byte & 0x80:
                break

        return data



class BaseClient:
    def __init__(self, host="localhost", port=25565, timeout=5, version=47):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.varint = VarInt()
        self.connected = False
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
            self.host,
            25565,
            self.varint.pack(next_state)# next state 1 for status request
        )
        packet = Packet(fields)
        packet = packet.pack()
        self._send(packet)