
__author__ = "Sch8ill"

import struct
from varint import VarInt


class Packet:
    def __init__(self, id, fields=[]):
        self.id = id
        self.fields = fields
        self.varint = VarInt()


    def pack(self):
        packet = self._encode(self.id)

        for field in self.fields:
            field = self._encode(field)
            packet += field

        packet = self.varint.pack(len(packet)) + packet
        return packet


    def _encode(self, data):
        if type(data) == int:
            data = struct.pack("H", data)

        elif type(data) == str:
            data = data.encode("utf-8")
            data = self.varint.pack(len(data)) + data

        elif type(data) == float:
            print(data)
            data = struct.pack(">Q", int(data))
            print(data)

        return data