
import struct

class QueryPacket:
    def __init__(self, type, session_id, payload):
        self.type = type
        self.session_id = session_id
        self.payload = payload


    def pack(self):
        packet = b"\xFE\xFD" # some padding
        packet += struct.pack("!B", self.type)
        packet +=  struct.pack('>l', self.session_id)
        packet += self.payload
        return packet

