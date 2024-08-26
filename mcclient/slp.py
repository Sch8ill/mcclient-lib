import json

from mcclient.base_client import BaseClient, DEFAULT_PORT, DEFAULT_TIMEOUT, DEFAULT_PROTO
from mcclient.packet import OutboundPacket, InboundPacket
from mcclient.response import SLPResponse, LegacySLPResponse


class SLPClient(BaseClient):
    def __init__(self, host: str, port: int = DEFAULT_PORT, timeout: int = DEFAULT_TIMEOUT, proto: int = DEFAULT_PROTO,
                 srv: bool = True):
        super().__init__(host=host, port=port, timeout=timeout, proto=proto, srv=srv)

    def get_status(self) -> SLPResponse:
        self._connect()
        self._handshake()
        res = self._status_request()
        return SLPResponse(self.address.get_host(), self.address.get_port(), res)

    def _status_request(self) -> dict:
        req = OutboundPacket(0)
        req.write(self.sock)

        packet = InboundPacket(self.sock)
        res = packet.read_string()

        self._close()
        return json.loads(res)


class LegacySLPClient(BaseClient):
    def __init__(self, host: str, port: int = 25565, timeout: int = 5):
        super().__init__(host=host, port=port, timeout=timeout)

    def get_status(self) -> LegacySLPResponse:
        self._connect()
        # legacy status request
        self.sock.send(b"\xFE\x01")
        raw_res = self.sock.recv(1024)
        self._close()

        # remove padding and other headers
        res_bytes = raw_res[3:]
        res_str = res_bytes.decode("UTF-16-be", errors="ignore")
        res_split_str = res_str.split("\x00")
        res = LegacySLPResponse(self.address.get_host(), self.address.get_port(), res_split_str)
        return res
