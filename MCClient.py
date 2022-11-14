#!/usr/bin/env python3

__version__ = "0.1.9"
__author__ = "Sch8ill"

from clients.query import QueryClient
from clients.slp import SLPClient



class MCClient:
    def __init__(self, host="localhost", port="25565", timeout=0.5):
        self.host = host
        self.port = port
        self.timeout = timeout


    def ping(self):
        client = SLPClient(self.host, self.port, timeout=self.timeout)
        return client.get_status()


    def query(self):
        client = QueryClient(self.host, self.port, timeout=self.timeout)
        return client.get_stats()



if __name__ == "__main__":
    client = MCClient(host="185.14.95.45", port=29565)
    slp = client.ping()
    q = client.query()

    print(slp)
    print(q)




    # {'previewsChat': False, 'enforcesSecureChat': False, 'description': {'extra': [{'text': 'Ich verkaufe meinen Server, ganz ganz billig, heute Nacht!'}], 'text': ''}, 'players': {'max': 69, 'online': 1, 'sample': [{'id': 'd40e6959-872b-47ae-96f6-0377451fd61e', 'name': 'Sch8ill'}]}, 'version': {'name': 'Spigot 1.19.2', 'protocol': 760}}
    # {'motd': 'Ich verkaufe meinen Server, ganz ganz billig, heute Nacht!', 'gametype': 'SMP', 'game_id': 'MINECRAFT', 'version': '1.19.2', 'plugins': [], 'map': 'world', 'numplayers': 1, 'maxplayers': 69, 'hostport': 29565, 'hostip': '172.18.0.2', 'software': 'CraftBukkit on Bukkit 1.19.2-R0.1-SNAPSHOT', 'players': ['Sch8ill']}