import dns.resolver


class Address:
    def __init__(self, addr, proto="tcp"):
        self.addr = addr
        self.proto = proto
        self.is_ip = self._ip_check(self.addr)


    def get_host(self, srv=True):
        if self.is_ip:
            return self.addr, None

        else:
            return self._resolve_hostname(self.addr, srv)


    def _resolve_hostname(self, hostname, srv):
        host = self._resolve_a_record(hostname)
        srv_record = None
        if srv:
            try:
                srv_record = self._mc_srv_lookup(hostname, self.proto)
                srv = True
                
            except Exception:
                pass

        if srv_record != None:
            return host, srv_record[1]

        else:
            return host, None


    @staticmethod
    def _mc_srv_lookup(hostname, proto):
        srv_prefix = f"_minecraft._{proto}."
        srv_record = dns.resolver.resolve(srv_prefix + hostname, "SRV")[0] # only use the first srv record returned
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