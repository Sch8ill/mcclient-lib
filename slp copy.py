#!/usr/bin/env python3

__version__ = "0.2.5"
__author__ = "Sch8ill"


import socket
import json
import time
import struct


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



class Packet:
    def __init__(self, fields=[]):
        self.fields = fields
        self.varint = VarInt()


    def pack(self):
        packet = b""
        for field in self.fields:
            field = self._encode(field)
            packet += field

        packet = self.varint.pack(len(packet)) + packet # add packetlength
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
        self.connected = False
        self.retries = 0
        self.sock.settimeout(timeout)
        self.varint = VarInt()
        self.protocoll_version = self.varint.pack(4)


    def _connect(self):
        if self.connected == False: # adds ability to "implant" an alredy connected socket, usefull for scanning
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


    def _flush(self, length=8192):
        self.sock.recv(length)


    def _handshake(self, next_state=1):
        fields = [
            b"\x00", # packet id
            self.protocoll_version,
            self.host,
            25565,
            self.varint.pack(next_state)# next state 1 for status request
        ]
        packet = Packet(fields)
        packet = packet.pack()
        self._send(packet)


    def legacy_ping(self):
        self._connect()
        self._send(b"\xFE") # legacy status request
        raw_res = self._recv()

        self.sock.close()
        self.connected = None

        res = raw_res[2][1:] # remove padding and other headers
        res = res.decode("UTF-16", errors="ignore")
        data = {}
        res = res.split("§") # data is split with "§"

        data["motd"] = "".join(res[:-2])
        data["online"] = int(res[-2])
        data["max"] = int(res[-1])
        return data


    def _status_request(self):
        packet = Packet([b"\x00"]) # send status request
        packet = packet.pack()
        self._send(packet)
        res = self._recv()

        if res[0]:
            if self.retries < 3:
                self.retries += 1
                self._flush()
                self._status_request()

            else:
                raise Exception("Max retries exceeded.")

        self.sock.close()
        self.connected = None

        res = res[2][2:]
        res = res.decode("utf-8")
        res = json.loads(res)
        self.retries = 0

        return res


    def get_stats(self):
        try:
            self._connect()
            self._handshake() # handshake + set connection state
            return self._status_request()

        except Exception as e:
            return e
