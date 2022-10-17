#!/usr/bin/env python3

__version__ = "0.1.0"
__author__ = "Sch8ill"

import socket
import struct
import random


class Packet:
    def __init__(self, type, session_id, payload):
        self.type = type
        self.session_id = session_id
        self.payload = payload


    def pack(self):
        packet = b"\xFE\xFD"
        packet += struct.pack("B", self.type)
        packet +=  struct.pack('>l', self.session_id)
        packet += self.payload

        return packet




class QueryClient:
    def __init__(self, host="localhost", port=25565):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(8)
        self.session_id = 1 #random.randint(1, 69)##############################################################


    def _handshake(self):
        packet_type = 9
        packet = Packet(
            packet_type,
            self.session_id,
            b""
        )
        packet = packet.pack()
        self._send(packet)
        res = self._recv()
        self.token = struct.pack('>l', int(res[2][:-1]))
        print(self.token)
        
        


    def _send(self, packet):
        print("send: " + str(packet))
        return self.sock.sendto(packet, (self.host, self.port))


    def _recv(self):
        res = self.sock.recv(2048)
        print("received: " + str(res))
        type = res[0]
        session_id = res[1:5]
        payload = res[5:]
        return type, session_id, payload









if __name__ == "__main__":
    c = QueryClient()
    c._handshake()