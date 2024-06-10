# MCClient-lib

[![Downloads](https://static.pepy.tech/badge/mcclient-lib)](https://pepy.tech/project/mcclient-lib)
[![PyPI](https://img.shields.io/pypi/v/mcclient-lib?color=green&label=PyPI%20package)](https://pypi.org/project/mcclient-lib/)

A lightweight Minecraft client for querying the status data of a Minecraft server.

## Supported Minecraft versions

* Minecraft Java (v1.4.0 and later)
* Minecraft Bedrock

## Supported protocols

* [ServerListPing](https://wiki.vg/Server_List_Ping) for Minecraft Java servers
* [Legacy ServerListPing](https://wiki.vg/Server_List_Ping#1.4_to_1.5) for Minecraft Java servers before 1.4
* [Query Protocol](https://wiki.vg/Query) for Minecraft Java servers (this needs to be enabled on the server)
* [Bedrock ServerListPing](https://wiki.vg/Raknet_Protocol#Unconnected_Ping) for Minecraft Bedrock servers

## Installation

### pip

```bash
pip install mcclient-lib
```

## Usage

### ServerListPing

```python
from mcclient import SLPClient

# for Minecraft Java servers from version 1.7.0 and later
slp_client = SLPClient("mc.example.com")
res = slp_client.get_status()
 ```

### Query

```python
from mcclient import QueryClient

# for Minecraft Java servers (needs to be enabled on the server)
query_client = QueryClient("mc.example.com")
res = query_client.get_status()
```

### Bedrock ServerListPing

```python
from mcclient import BedrockSLPClient

# for Minecraft Bedrock servers
bedrock_slp_client = BedrockSLPClient("mc.example.com")
res = bedrock_slp_client.get_status()
```

### Response

How to handle the returned response object

```python
print(f"host: {res.host}")
print(f"port: {res.port}")
print(f"motd: {res.motd}")

print(f"online players: {res.players.online}")
print(f"max players: {res.players.max}")
print(f"players list: {res.players.list}")

print(f"version: {res.version.name}")
print(f"protocol version: {res.version.protocol}")

print(f"timestamp: {res.timestamp}")
print(f"favicon: {res.favicon is not None}")

# only for query and Bedrock responses
print(f"gametype: {res.gametype}")
print(f"map: {res.map}")

# only for query responses
print(f"plugins: {res.plugins}")
print(f"host ip: {res.hostip}")
print(f"host port: {res.hostport}")

# only for bedrock responses
print(f"server id: {res.server_id}")
```

## Queryable data

* MOTD
* Online player count
* Max player count
* Player list
* Server version
* Server protocol version
* Mods and plugins
* Has a favicon
* Name of the map
* Hostport and hostip
* Gametype
* Server ID

Note that not every field is queryable with every protocol.

## Documentation

You can find more documentation [here](https://github.com/Sch8ill/MCClient-lib/blob/master/docs.md "/docs.md"), feel free to look into the [source](https://github.com/Sch8ill/MCClient-lib "github.com/Sch8ill/MCClient-lib") if you can't find enough.
