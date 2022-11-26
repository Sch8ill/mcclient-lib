
import struct


class VarInt: # class to pack and unpack Varints
    @staticmethod
    def pack(data):
        ordinal = b''
        while data != 0:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))
        return ordinal


    @staticmethod
    def unpack(sock):
        data = 0
        for i in range(5):
            ordinal = sock.recv(1)
            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7*i
            if not byte & 0x80:
                break

        return data




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
            data = struct.pack("H", data)

        elif type(data) == str:
            data = data.encode("utf-8")
            data = self.varint.pack(len(data)) + data

        elif type(data) == float:
            print(data)
            data = struct.pack(">Q", int(data))
            print(data)
        return data