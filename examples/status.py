# sample script to get a servers status using SLP
from mcclient import SLPClient

client = SLPClient("mc.lpmitkev.de") # sample server
res = client.get_status()

for key in res.res:
    print(f"{key}: {res.res[key]}")