#!/usr/bin/env python3

__version__ = "0.1.2"
__author__ = "Sch8ill"


import socket
import json
import time
import struct



class VarInt:
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



class Packet:
    def __init__(self, id, fields=[]):
        self.id = id
        self.fields = fields
        self.varint = VarInt()


    def pack(self):
        packet = self._encode(self.id)

        for field in self.fields:
            field = self._encode(field)
            packet += field

        packet = self.varint.pack(len(packet)) + packet
        return packet


    def _encode(self, data):
        if type(data) == int:
            data = struct.pack("H", data)

        elif type(data) == str:
            data = data.encode("utf-8")
            data = self.varint.pack(len(data)) + data

        elif type(data) == float:
            print(data)
            data = struct.pack(">Q", int(data))
            print(data)

        return data



class SLPClient:
    def __init__(self, host="localhost", port=25565, timeout=5):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.protocoll_version = b"\x00"
        self.varint = VarInt()


    def _connect(self):
        self.sock.connect((self.host, self.port))


    def _send(self, packet, verbose=False):
        if verbose:
            print("send: " + str(packet))

        return self.sock.send(packet)


    def _recv(self, extra_varint=False):
        length = self.varint.unpack(self.sock)
        packet_id = self.varint.unpack(self.sock)
        data = b""

        if extra_varint:
            if packet_id > length:
                self._unpack_varint(self.sock)

            extra_length = self.varint.unpack(self.sock)

            while len(data) < extra_length:
                data += self.sock.recv(extra_length)

        else:
            data = self.sock.recv(length)

        return data


    def _handshake(self, next_state=b"\x01"):
        fields = [
            self.protocoll_version,
            self.host,
            25565,
            next_state
        ]

        packet = Packet(b"\x00", fields)
        packet = packet.pack()
        self._send(packet)


    def get_status(self):
        self._connect()
        self._handshake()

        packet = Packet(b"\x00")
        packet = packet.pack()
        self._send(packet)
        res = self._recv(extra_varint=True)

        res = res.decode("utf-8")
        res = json.loads(res)

        self.sock.close()

        return res




if __name__ == "__main__":
    client = SLPClient(host="185.14.95.45", port=29565)
    res = client.get_status()
    print(res)
    
    