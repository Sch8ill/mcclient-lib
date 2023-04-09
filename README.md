# MCClient

[![Downloads](https://static.pepy.tech/badge/mcclient-lib)](https://pepy.tech/project/mcclient-lib)
[![PyPI](https://img.shields.io/pypi/v/mcclient-lib?color=green&label=PyPI%20package)](https://pypi.org/project/mcclient-lib/)

A lightweight Minecraft client for querying the status data of a Minecraft server.

## Supported Mincraft versions

* Minecraft Java (v1.4.0 and newer)
* Minecraft Bedrock

## Supported protocols

* [ServerListPing](https://wiki.vg/Server_List_Ping "wiki.vg/Server_List_Ping") for Minecraft java servers
* [Legacy ServerListPing](https://wiki.vg/Server_List_Ping#1.4_to_1.5 "wiki.vg/Server_List_Ping#1.4_to_1.5") for Minecraft java servers before 1.4
* [Query Protocol](https://wiki.vg/Query "wiki.vg/Query") for Minecraft java servers (this needs to be enabled on the server)
* [Bedrock ServerListPing](https://wiki.vg/Raknet_Protocol#Unconnected_Ping "wiki.vg/Raknet_Protocol#Unconnected_Ping") for Bedrock servers

## Installation

### pypi

```bash
pip3 install mcclient-lib
```

### pip + github

 You can also install the package directly from github.

 ```bash
 pip3 install git+https://github.com/Sch8ill/MCClient-lib.git
 ```

## Usage

### ServerListPing

```python
from mcclient import SLPClient

# for Minecraft Java servers from 1.7.* and newer
slp_client = SLPClient("mc.example.com", port=12345)
res = slp_client.get_status()
 ```

### Query

```python
from mcclient import QueryClient

# for Minecraft Java servers (needs to be enabled on the server)
query_client = QueryClient("mc.example.com", port=12345)
res = query_client.get_status()
```

### Bedrock ServerListPing

```python
from mcclient import BedrockSLPClient

# for Minecraft Bedrock servers
bedrock_slp_client = BedrockSLPClient("mc.example.com", port=12345)
res = bedrock_slp_client.get_status()
```

### Response

How to handle the returned response object

```python
# The server address and port
host = res.host
port = host.port

motd = res.motd

online_players = res.players.online
max_players = res.players.max
player_list = res.players.list

version = res.version.name
protocol_version = res.version.protocol

# only for query responses
plugins = res.plugins

# only for basic ServerListPing
has_favicon = res.favicon

# only for query and Bedrock
gametype = res.gametype

# only for query and bedrock
map = res.map

# only for bedrock
server_id = res.server_id

# timestamp of the request
timestamp = res.timestamp

# the reponse as a dictonary with some further infomation
# the keys are named like the values in the response object
res_dictionary = res.res
```

## Queryable data

* motd
* online player count
* max player count
* player list
* server version
* server protocol version
* mods and plugins
* has a favicon
* name of map
* hostport and hostip
* gametype
* server id

Note: not every field is queryable with every protocol.

## Documentation

You can find more documentation [here](https://github.com/Sch8ill/MCClient-lib/blob/master/docs.md "/docs.md"), feel free to look into the [source](https://github.com/Sch8ill/MCClient-lib "github.com/Sch8ill/MCClient-lib") if you can't find enough.