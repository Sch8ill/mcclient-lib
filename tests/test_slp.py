import json

from mcclient import SLPClient, LegacySLPClient
from mcclient.encoding.packet import Packet

from tests.utils import BaseTestConn, TooManyPackets

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


class SLPTestConn(BaseTestConn):
    max_packets = 2

    def __init__(self, hostname, base_res, proto):
        super().__init__()
        self.hostname = hostname
        self.base_res = base_res
        self.proto = proto


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
            self.respond_res()

        elif self.packets >= self.max_packets:
            raise TooManyPackets(self.max_packets)


    def respond_res(self):
        res_fields = (
            b"\x00",
            json.dumps(self.base_res)
        )
        packet = Packet(res_fields).pack()
        self.respond(packet)



def test_slp_request():
    test_conn = SLPTestConn(TEST_HOSTNAME, BASE_RES, TEST_PROTO)
    slp_client = SLPClient(TEST_HOSTNAME, proto=TEST_PROTO)
    slp_client.implant_socket(test_conn)
    slp_client.get_status()



class LegaySLPTestConn(BaseTestConn):
    max_packets = 1

    def __init__(self, base_res):
        super().__init__()
        self.base_res = base_res


    def send(self, data):
        if self.packets == 0:
            self.packets += 1
            assert data == b"\xFE\x01"

            test_res = b"""\xFF\x00\x25\x00\xA7\x00\x31\x00\x00\x00
                \x31\x00\x32\x00\x37\x00\x00\x00\x31\x00\x2E\x00\x31
                \x00\x39\x00\x2E\x00\x33\x00\x00\x00\x41\x00\x20\x00
                \x4D\x00\x69\x00\x6E\x00\x65\x00\x63\x00\x72\x00\x61
                \x00\x66\x00\x74\x00\x20\x00\x53\x00\x65\x00\x72\x00
                \x76\x00\x65\x00\x72\x00\x00\x00\x30\x00\x00\x00\x32
                \x00\x30"""
            # test packet dump from raw leagy slp response, SHOULD be changed in the future!!
            self.respond(test_res)

        elif self.packets >= self.max_packets:
            raise TooManyPackets(self.max_packets)



def test_legacy_slp_request():
    test_conn = LegaySLPTestConn(BASE_RES)
    legacy_slp_client = LegacySLPClient(TEST_HOSTNAME)
    legacy_slp_client.implant_socket(test_conn)
    legacy_slp_client.get_status()