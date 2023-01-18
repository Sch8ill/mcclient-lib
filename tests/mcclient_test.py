import struct

from mcclient import SLPClient
from mcclient.address import Address
from mcclient.encoding.varint import VarInt
from mcclient.encoding.packet import Packet

def varint_test():
    # encoding
    enc_test_values = [1, 127, 128, 255]
    enc_test_results = [b"\x01", b"\x7f", b"\x80\x01", b"\xff\x01"]
    varint = VarInt()

    for value, result in zip(enc_test_values, enc_test_results):
        encoded_value = varint.pack(value)
        assert encoded_value == result


def packet_encoding_test():
    test_result = b"\x1A\x01\x15\x74\x68\x69\x73\x20\x69\x73\x20\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6E\x67\x01\x00\x00"
    test_fields = (
        b"\x01",
        "this is a test string",
        "\x00",
        False
        )
    test_packet = Packet(test_fields)
    enc_test_packet = test_packet.pack()
    assert enc_test_packet == test_result


def address_test():
    test_domain = Address("google.com").get_host()
    # add more tests for test_domain

    test_ip = Address("23.23.23.23").get_host()
    assert test_ip[0] == "23.23.23.23"

    test_srv_record = Address("pokecentral.org").get_host() # random server for testing, needs to be changed!
    assert test_srv_record[1] == 25565



class SLPTestSocket:
    def __init__(self):
        self.buffer = b""

    def send(self, data):
        self.on_send(data)


    def recv(self, length):
        data = self.buffer[0:length]
        self.buffer = self.buffer[length:]
        return data


    def on_send(self, data):
        


def slp_test():
    test_sock = SLPTestSocket()
    slp_client = SLPClient("example.com")
    slp_client.implant_socket(test_sock)



if __name__ == "__main__":
    varint_test()
    packet_encoding_test()
    address_test()