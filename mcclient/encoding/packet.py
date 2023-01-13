import struct
from mcclient.encoding.varint import VarInt


class Packet:
    def __init__(self, fields=[]):
        self.fields = fields
        self.varint = VarInt()


    def pack(self):
        packet = b""
        for field in self.fields:
            field = self._encode(field)
            packet += field

        packet = self.varint.pack(len(packet)) + packet # add packetlength
        return packet


    def _encode(self, data):
        if type(data) == int:
            data = struct.pack(">H", data)

        elif type(data) == str:
            data = data.encode("utf-8")
            data = self.varint.pack(len(data)) + data

        elif type(data) == bool:
            data = b"\x01" if data else b"\x00"

        elif type(data) == float:
            print(data)
            data = struct.pack(">Q", int(data))
            print(data)
        return data