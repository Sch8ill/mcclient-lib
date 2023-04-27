# sample script to get a servers status using SLP
from mcclient import SLPClient

client = SLPClient("<YOUR_SERVER_ADDRESS>")
res = client.get_status()

for key in res.res:
    print(f"{key}: {res.res[key]}")
