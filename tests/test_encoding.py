from mcclient.packet import OutboundPacket, varint


def test_varint_encoding():
    enc_test_values = [1, 127, 128, 255]
    enc_test_results = [b"\x01", b"\x7f", b"\x80\x01", b"\xff\x01"]

    for value, result in zip(enc_test_values, enc_test_results):
        encoded_value = varint.pack(value)
        assert encoded_value == result


def test_packet_encoding():
    test_result = b"\x19\x01\x15this is a test string\x00\x00"

    test_packet = OutboundPacket(1)
    test_packet.write_string("this is a test string")
    test_packet.write_varint(0)
    test_packet.write_bool(False)

    assert test_result == test_packet.pack()
