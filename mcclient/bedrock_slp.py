
import socket
import struct
from mcclient.address import Address
from mcclient.response import BedrockResponse


class BedrockSLPClient:
    def __init__(self, host, port=19132, timeout=4):
        self.get_host(host, port)
        self.timeout = timeout


    def get_host(self, hostname, port):
        addr = Address(hostname, proto="udp")
        addr = addr.get_host()
        self.hostname = hostname
        self.host = addr[0]
        if addr[1] == None:
            self.port = port

        else:
            self.port = addr[1]


    def get_status(self):
        res = self._request_status()
        res = self._parse_res(res)
        return BedrockResponse(self.hostname, self.port, res)

    
    def _request_status(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        status_request = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx"
        sock.sendto(status_request, (self.host, self.port))
        data, _ = sock.recvfrom(4096)
        return data


    @staticmethod
    def _parse_res(res):
        res = res[1:]
        extra_len = struct.unpack(">H", res[32:34])[0]
        res = res[34 : 34 + extra_len]
        res = res.decode()
        res = res.split(";")
        return res