import struct

from mcclient.encoding.varint import pack_varint


class Packet:
    fields: tuple

    def __init__(self, *fields):
        self.fields = fields

    def pack(self) -> bytes:
        packet = b""
        for field in self.fields:
            packet += self._encode(field)

        # add the packet length
        return pack_varint(len(packet)) + packet

    @staticmethod
    def _encode(data) -> bytes:
        if isinstance(data, str):
            str_bytes = data.encode("utf-8")
            return pack_varint(len(str_bytes)) + str_bytes

        elif isinstance(data, bytes):
            return data

        elif isinstance(data, bool):
            return b"\x01" if data else b"\x00"

        raise TypeError(f"Type {type(data)} cannot be encoded")


class QueryPacket:
    type: int
    session_id: int
    payload: bytes

    def __init__(self, type: int, session_id: int, payload: bytes):
        self.type = type
        self.session_id = session_id
        self.payload = payload

    def pack(self) -> bytes:
        packet = b"\xFE\xFD"  # query packet padding
        packet += struct.pack("!B", self.type)
        packet += struct.pack('>l', self.session_id)
        packet += self.payload
        return packet
