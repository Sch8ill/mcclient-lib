
__author__ = "Sch8ill"

from mcclient import QueryClient
from mcclient import SLPClient



slp_client = SLPClient(host="mc.lpmitkev.de", port=25565) # random server

query_client = QueryClient(host="mc.lpmitkev.de", port=25565)


print(slp_client.get_stats())

print(slp_client.legacy_ping())

print(query_client.get_stats())