import json

from mcclient import SLPClient
from mcclient.encoding.varint import VarInt
from mcclient.encoding.packet import Packet

TEST_PROTO = 47
TEST_HOSTNAME = "example.com"
BASE_RES = {
        "description" : {
            "text": "This is an example motd"
        },
        "version": {
            "name": "1.19.2",
            "protocol": 795
        },
        "players": {
            "max": 69,
            "online": 5,
            "sample": [
                {
                "name": "thinkofdeath",
                "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"
                }
            ]
        },
        "previewsChat": True,
        "enforcesSecureChat": True
    }


class SLPTestSocket:
    varint = VarInt()

    def __init__(self, hostname, base_res, proto):
        self.hostname = hostname
        self.base_res = base_res
        self.proto = proto
        self.buffer = b""
        self.packets = 0

    def send(self, data):
        if self.packets == 0:
            self.packets += 1
            fields = (
                b"\x00", # packet id
                self.varint.pack(self.proto),
                self.hostname,
                25565,
                self.varint.pack(1)
            )
            test_packet = Packet(fields).pack()
            assert data == test_packet

        elif self.packets == 1:
            self.packets += 1
            assert data == b"\x01\x00"
            self.respond()

        elif self.packets > 2:
            raise Exception("Received too many packet (more than 2)")


    def recv(self, length):
        data = self.buffer[:length]
        self.buffer = self.buffer[length:]
        return data


    def close(self):
        pass


    def respond(self):
        res_fields = (
            b"\x00",
            json.dumps(self.base_res)
        )
        packet = Packet(res_fields).pack()
        self.buffer += packet


def test_slp():
    test_sock = SLPTestSocket(TEST_HOSTNAME, BASE_RES, TEST_PROTO)
    slp_client = SLPClient(TEST_HOSTNAME, proto=TEST_PROTO)
    slp_client.implant_socket(test_sock)
    res = slp_client.get_status()