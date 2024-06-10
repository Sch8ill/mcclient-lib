from mcclient.encoding.packet import Packet
from mcclient.encoding.varint import pack_varint


def test_varint_encoding():
    # encoding
    enc_test_values = [1, 127, 128, 255]
    enc_test_results = [b"\x01", b"\x7f", b"\x80\x01", b"\xff\x01"]

    for value, result in zip(enc_test_values, enc_test_results):
        encoded_value = pack_varint(value)
        assert encoded_value == result


def test_packet_encoding():
    test_result = (b"\x1A\x01\x15\x74\x68\x69\x73\x20\x69\x73\x20\x61\x20\x74\x65\x73\x74\x20\x73\x74\x72\x69\x6E\x67"
                   b"\x01\x00\x00")
    test_packet = Packet(
        b"\x01",
        "this is a test string",
        "\x00",
        False
    )
    assert test_result == test_packet.pack()
