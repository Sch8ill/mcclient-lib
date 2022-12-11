#!/usr/bin/env python3

__author__ = "Sch8ill"


import json
import socket
from mcclient.client import BaseClient
from mcclient.utils import Packet, VarInt




class SLPClient(BaseClient):
    def __init__(self, host="localhost", port=25565, timeout=5):
        super().__init__(host=host, port=port, timeout=timeout)
        self.retries = 0


    def legacy_ping(self): # Todo: implement packetloss handling
        self._connect()
        self._send(b"\xFE") # legacy status request
        raw_res = self._recv()

        self._close()

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

        if res[0]: # if packetloss accured
            if self.retries < 3:
                self.retries += 1
                self._reset()
                return self._status_request()

            else:
                raise Exception("Max retries exceeded.")

        self._close(flush=False)

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