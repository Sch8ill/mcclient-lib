
__author__ = "Sch8ill"

from mcclient import QueryClient
from mcclient import SLPClient
from mcclient import BedrockSLPClient



slp_client = SLPClient(host="mc.lpmitkev.de", port=25565) # random server

query_client = QueryClient(host="mc.lpmitkev.de", port=25565)

bedrock_client = BedrockSLPClient("mcprison.com")

print("bedrock: " + str(bedrock_client.get_stats().res))

print("slp: " + str(slp_client.get_stats().res))

print("legacy slp: " + str(slp_client.legacy_ping().res))

print("query: " + str(query_client.get_stats().res))