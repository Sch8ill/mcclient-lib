# sample script to get a servers status using SLP
from mcclient import SLPClient

client = SLPClient("hypixel.net")
res = client.get_status()

print(f"host: {res.host}")
print(f"port: {res.port}")
print(f"motd: {res.motd}")

print(f"online players: {res.players.online}")
print(f"max players: {res.players.max}")
print(f"players list: {res.players.list}")

print(f"version: {res.version.name}")
print(f"protocol version: {res.version.protocol}")

print(f"favicon: {res.favicon is not None}")
print(f"timestamp: {res.timestamp}")
