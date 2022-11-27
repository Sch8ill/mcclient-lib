#!/usr/bin/env python3

__author__ = "Sch8ill"


import json
from client import BaseClient
from utils import Packet




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