#!/usr/bin/env python3

__version__ = "0.2.0"
__author__ = "Sch8ill"


import socket
import struct
import random

class Packet:
    def __init__(self, type, session_id, payload):
        self.type = type
        self.session_id = session_id
        self.payload = payload


    def pack(self):
        packet = b"\xFE\xFD" # every packet starts with this, blame mojang
        packet += struct.pack("!B", self.type)
        packet +=  struct.pack('>l', self.session_id)
        packet += self.payload
        return packet



class QueryClient:
    def __init__(self, host="localhost", port=25565, timeout=0.5):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)


    def _handshake(self):
        self.session_id = random.randint(0, 2147483648) & 0x0F0F0F0F # generate session id from int between 0 and 2147483648
        packet = Packet(
            9, # type 9 for handshaking
            self.session_id,
            b"" # empty payload for handshaking
        )
        packet = packet.pack()
        self._send(packet)
        res = self._recv()
        self.token = struct.pack('>l', int(res[2][:-1])) # extract token from response


    def get_stats(self):
        self._handshake()
        payload = self.token + b"\x00\x00\x00\x00" # challenge token and some padding for full stat request
        packet = Packet(
            0, # packettype 0 for stat request
            self.session_id,
            payload
        )
        packet = packet.pack()
        self._send(packet)
        res = self._recv()
        return self._read_query(res)


    @staticmethod
    def _read_query(res):
        res = res[2][11:] # remove unnecessary padding
        stats, players = res.split(b"\x00\x00\x01player_\x00\x00") # split stats from players
        data = {}

        stats = stats.split(b"\x00")
        stats = [stat.decode("utf-8") for stat in stats] # decode keys and values
        stats[0] = "motd" # replace "hostname" with "motd"
        key = True
        for y, x in enumerate(stats):
            if key:
                data[x] = stats[y + 1]
                key = False

            else:
                key = True

        for key in ["numplayers", "maxplayers", "hostport"]: # convert strings to ints
            data[key] = int(data[key])

        data["software"] = "Vanilla"
        software_parts = data["plugins"].split(":", 1)
        data["software"] = software_parts[0].strip()
        if len(software_parts) == 2:
            data["plugins"] = [plugin.strip() for plugin in software_parts[1].split(";")]

        else:
            data["plugins"] = []

        players = players[:-2] # remove endpadding
        players = players.split(b"\x00") # split players
        data["players"] = [player.decode("utf-8") for player in players if player != b""] # decode players
        return data
        

    def _send(self, packet):
        return self.sock.sendto(packet, (self.host, self.port))


    def _recv(self):
        res = self.sock.recv(4096)
        type = res[0]
        session_id = res[1:5]
        payload = res[5:]
        return type, session_id, payload