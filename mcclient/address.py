import ipaddress

import dns.resolver


class Address:
    host: str
    port: int
    srv_host: str
    srv_port: int
    srv: bool

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.srv = False

    def resolve(self) -> None:
        if self.is_ip():
            return

        try:
            record = dns.resolver.resolve("_minecraft._tcp." + self.host, "SRV")[0]
            self.srv_host = str(record.target).rstrip(".")
            self.srv_port = record.port
            self.srv = True

        except Exception:
            pass

    def address(self) -> tuple[str, int]:
        return self.get_host(), self.get_port()

    def get_host(self) -> str:
        if self.srv:
            return self.srv_host

        return self.host

    def get_port(self) -> int:
        if self.srv:
            return self.srv_port

        return self.port

    def is_ip(self) -> bool:
        try:
            ipaddress.ip_address(self.host)
            return True

        except ValueError:
            return False
