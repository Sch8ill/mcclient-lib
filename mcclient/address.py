
import dns.resolver



class Address:
    def __init__(self, addr):
        self.addr = addr
        self.is_ip = self._ip_check(self.addr)


    def get_host(self):
        if self.is_ip:
            return self.addr

        else:
            return self._resolve_a_record(self.addr)

    @staticmethod
    def _mc_srv_lookup(hostname):
        srv_prefix = "_minecraft._tcp."
        srv_record = dns.resolver.resolve(srv_prefix + hostname, "SRV")[0]# only use the first srv record returned
        host = str(srv_record.target).rstrip(".")
        port = int(srv_record.port)
        return host, port


    @staticmethod
    def _resolve_a_record(hostname):
        record = dns.resolver.resolve(hostname, "A")[0]
        return str(record).rstrip(".")


    @staticmethod
    def _ip_check(addr):
        is_ip = True
        if addr.count(".") == 3:
            for octet in addr.split("."):
                try:
                    octet = int(octet)
                    if not octet <= 255 and octet >= 0:
                        is_ip = False
                        break

                except ValueError:
                    is_ip = False

        else:
            is_ip = False
        return is_ip