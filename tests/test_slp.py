import json

from mcclient import SLPClient
from mcclient.packet import OutboundPacket
from tests.utils import TooManyPackets, BaseTestConn, create_mock_socket

TEST_PROTO = 47
TEST_HOSTNAME = "example.com"
TEST_PORT = 25565
BASE_RES = {
    "description": {
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

            test_packet = OutboundPacket(0)
            test_packet.write_varint(self.proto)
            test_packet.write_string(self.hostname)
            test_packet.write_ushort(TEST_PORT)
            test_packet.write_varint(1)

            assert data == test_packet.pack()

        elif self.packets == 1:
            self.packets += 1
            assert data == b"\x01\x00"
            self.respond_res()

        elif self.packets >= self.max_packets:
            raise TooManyPackets(self.max_packets)

    def respond_res(self):
        packet = OutboundPacket(0)
        packet.write_string(json.dumps(self.base_res))
        self.respond(packet.pack())


def test_slp_request():
    socket = create_mock_socket(SLPTestConn)
    test_conn = socket.socket(TEST_HOSTNAME, BASE_RES, TEST_PROTO)
    slp_client = SLPClient(TEST_HOSTNAME, proto=TEST_PROTO)
    slp_client.implant_socket(test_conn)
    slp_client.get_status()
