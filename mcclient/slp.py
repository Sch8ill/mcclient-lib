
import json
from mcclient.base_client import BaseClient
from mcclient.response import SLPResponse
from mcclient.response import SLPLegacyResponse
from mcclient.encoding.varint import VarInt
from mcclient.encoding.packet import Packet



class SLPClient(BaseClient):
    def __init__(self, host="localhost", port=25565, timeout=5):
        super().__init__(host=host, port=port, timeout=timeout)
        self.retries = 0


    def legacy_ping(self): # Todo: implement packetloss handling
        self._connect()
        self._send(b"\xFE\x01") # legacy status request
        raw_res = self.sock.recv(1024)
        self._close()

        res = raw_res[3:] # remove padding and other headers
        res = res.decode("UTF-16-be", errors="ignore")
        res = res.split("\x00")
        res = SLPLegacyResponse(self.host, self.port, res)
        return res


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
        res = SLPResponse(self.host, self.port, res)
        self.retries = 0
        return res


    def get_stats(self):
        self._connect()
        self._handshake() # handshake + set connection state
        return self._status_request()