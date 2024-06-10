from mcclient import BedrockSLPClient

from tests.utils import BaseTestConn, TooManyPackets, create_mock_socket


class BedrockTestConn(BaseTestConn):
    max_packets = 1

    def __init__(self):
        super().__init__()

    def sendto(self, data, *args):
        if self.packets == 0:
            self.packets += 1
            example_req = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx"
            assert data == example_req

            example_res = (b"\x1C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xF2\xA6\x29\x24\xC3\xD2\x00\xFF\xFF\x00\xFE"
                           b"\xFE\xFE\xFE\xFD\xFD\xFD\xFD\x12\x34\x56\x78\x00\x63\x4D\x43\x50\x45\x3B\xC2\xA7\x62\xC2"
                           b"\xA7\x6C\x45\x55\x20\xC2\xA7\x37\xC2\xA7\x6C\xC2\xBB\x20\x42\x4C\x4F\x43\x4B\x20\x50\x41"
                           b"\x52\x54\x59\x20\xEE\x84\x87\x3B\x31\x32\x31\x3B\x31\x2E\x30\x3B\x39\x39\x31\x32\x3B\x31"
                           b"\x30\x30\x30\x30\x31\x3B\x2D\x36\x30\x30\x31\x32\x38\x38\x31\x32\x30\x37\x30\x37\x37\x33"
                           b"\x31\x36\x37\x33\x3B\x48\x69\x76\x65\x20\x47\x61\x6D\x65\x73\x3B\x53\x75\x72\x76\x69\x76"
                           b"\x61\x6C")
            self.respond(example_res)

        elif self.packets >= self.max_packets:
            raise TooManyPackets(self.max_packets)


def test_bedrock():
    socket = create_mock_socket(BedrockTestConn)
    test_conn = socket.socket()
    bedrock_client = BedrockSLPClient("example.com")
    bedrock_client.sock = test_conn  # implant test socket
    bedrock_client.get_status()
    # Todo: add checks for response
