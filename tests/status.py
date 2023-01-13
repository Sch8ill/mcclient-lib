from mcclient import QueryClient
from mcclient import SLPClient
from mcclient import LegacySLPClient
from mcclient import BedrockSLPClient



slp_client = SLPClient(host="mc.lpmitkev.de") # random server, SRV record test

legacy_slp_client = LegacySLPClient(host="mc.lpmitkev.de") # SRV record test

query_client = QueryClient(host="mc.lpmitkev.de")

bedrock_client = BedrockSLPClient("geo.hivebedrock.network")

print("bedrock: " + str(bedrock_client.get_status().res))

print("slp: " + str(slp_client.get_status().res))

print("legacy slp: " + str(legacy_slp_client.get_status().res))

print("query: " + str(query_client.get_status().res))