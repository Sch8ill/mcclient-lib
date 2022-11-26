#!/usr/bin/env python3

__author__ = "Sch8ill"

from query import QueryClient
from slp import SLPClient






slp_client = SLPClient(host="mc.lpmitkev.de", port=25565) # random server found through masscan
query_client = QueryClient(host="mc.lpmitkev.de", port=25565)

slp = slp_client.get_stats()
l_slp = slp_client.legacy_ping()
q = query_client.get_stats()

try:
    if "favicon" in slp:
        slp.pop("favicon")
except:
    pass

print(slp)
print(l_slp)
print(q)




# {'previewsChat': False, 'enforcesSecureChat': False, 'description': {'extra': [{'text': 'Ich verkaufe meinen Server, ganz ganz billig, heute Nacht!'}], 'text': ''}, 'players': {'max': 69, 'online': 1, 'sample': [{'id': 'd40e6959-872b-47ae-96f6-0377451fd61e', 'name': 'Sch8ill'}]}, 'version': {'name': 'Spigot 1.19.2', 'protocol': 760}}
# {'motd': 'Ich verkaufe meinen Server, ganz ganz billig, heute Nacht!', 'gametype': 'SMP', 'game_id': 'MINECRAFT', 'version': '1.19.2', 'plugins': [], 'map': 'world', 'numplayers': 1, 'maxplayers': 69, 'hostport': 29565, 'hostip': '172.18.0.2', 'software': 'CraftBukkit on Bukkit 1.19.2-R0.1-SNAPSHOT', 'players': ['Sch8ill']}