from mcclient import LegacySLPClient

from tests.utils import TooManyPackets, BaseTestConn, create_mock_socket

TEST_HOSTNAME = "example.com"


class LegacySLPTestConn(BaseTestConn):
    max_packets = 1

    def __init__(self):
        super().__init__()

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
            # test packet dump from a raw legacy slp response, SHOULD be changed in the future!!
            self.respond(test_res)

        elif self.packets >= self.max_packets:
            raise TooManyPackets(self.max_packets)


def test_legacy_slp_request():
    socket = create_mock_socket(LegacySLPTestConn)
    test_conn = socket.socket()
    legacy_slp_client = LegacySLPClient(TEST_HOSTNAME)
    legacy_slp_client.implant_socket(test_conn)
    legacy_slp_client.get_status()
