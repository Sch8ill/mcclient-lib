

from query import QueryClient
from slp import SLPClient



class MCClient:
    def __init__(self, host="localhost", port="25565"):
        self.host = host
        self.port = port


    def ping(self):
        client = SLPClient(self.host, self.port)
        return client.get_status()


    def query(self):
        client = QueryClient(self.host, self.port)
        return client.get_stats()



if __name__ == "__main__":
    client = MCClient(host="185.14.95.45", port=29565)
    slp = client.ping()
    q = client.query()

    print(slp)
    print(q)