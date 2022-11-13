#!/usr/bin/env python3

__version__ = "0.1.0"
__author__ = "Sch8ill"

import time
import socket
import struct
import random
import logging


class Packet:
    def __init__(self, type, session_id, payload):
        self.type = type
        self.session_id = session_id
        self.payload = payload


    def pack(self):
        packet = b"\xFE\xFD" # every packet starts with this, blame mojang
        packet += struct.pack("!B", self.type)
        packet +=  struct.pack('>l', self.session_id)
        packet += self.payload
        return packet




class QueryClient:
    def __init__(self, host="localhost", port=25565):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log = logging.getLogger("Queryclient")
        self.sock.settimeout(8)


    def _handshake(self):
        self.session_id = random.randint(0, 2147483648) & 0x0F0F0F0F # generate session id from int between 0 and 2147483648
        packet = Packet(
            9, # packettype 9 for handshaking
            self.session_id,
            b"" # empty payload
        )
        packet = packet.pack()
        self._send(packet)
        res = self._recv()
        self.token = struct.pack('>l', int(res[2][:-1])) # extract token from response
        self.log.debug("challenge token: " + str(self.token))


    def get_stats(self):
        self._handshake()

        payload = self.token + b"\x00\x00\x00\x00" # challenge token and four zero bytes for full stat request
        packet = Packet(
            0, # packettype 0 for stat resolving
            self.session_id,
            payload
        )
        packet = packet.pack()
        self._send(packet)
        res = self._recv()
        
        

    def _send(self, packet):
        self.log.debug("send: " + str(packet))
        return self.sock.sendto(packet, (self.host, self.port))


    def _recv(self):
        res = self.sock.recv(2048)
        self.log.debug("received: " + str(res))
        type = res[0]
        session_id = res[1:5]
        payload = res[5:]
        return type, session_id, payload









if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s", level=logging.NOTSET)

    s = time.time() * 1000

    c = QueryClient(host="185.14.95.45", port=29565)
    c.get_stats()

    print(time.time() * 1000 - s)