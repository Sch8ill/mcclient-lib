# MCClient
A lightweight Minecraft client to query the status of a Minecraft server.

### Supported Mincraft versions
* Minecraft Java (1.4.* -> 1.19.*)
* Minecraft Bedrock

### Supported protocols
* [Basic ServerListPing](https://wiki.vg/Server_List_Ping "wiki.vg/Server_List_Ping")
* [Legacy ServerListPing](https://wiki.vg/Server_List_Ping#1.4_to_1.5 "wiki.vg/Server_List_Ping#1.4_to_1.5")
* [Query Protocol (Full stat)](https://wiki.vg/Query "wiki.vg/Query")
* [Bedrock ServerListPing](https://wiki.vg/Raknet_Protocol#Unconnected_Ping "wiki.vg/Raknet_Protocol#Unconnected_Ping")

## Installation
### pypi
```bash
pip install mcclient-lib
```
The pypi package might not always be up to date.

## Usage
### Basic ServerListPing
```python
from mcclient import SLPClient

# for Minecraft Java servers from 1.7.*
slp_client = SLPClient("mc.example.com", port=12345)
res = slp_client.get_status()
print(res.motd)
 ```
### Query
```python
from mcclient import QueryClient

# for Minecraft Java servers (needs to be enabled on the server)
query_client = QueryClient(mc.example.com, port=12345)
res = query_client.get_status()
print(res.motd)
```

### Bedrock ServerListPing
```python
from mcclient import BedrockSLPClient

# for Minecraft Bedrock servers
bedrock_slp_client = BedrockSLPClient(mc.example.com, port=12345)
res = bedrock_slp_client.get_status()
print(res.motd)
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

## Documentation
There is some documentation [here](https://github.com/Sch8ill/MCClient-lib/blob/master/docs.md "/docs.md"), if that isn't enough just look into the [source](https://github.com/Sch8ill/MCClient-lib "github.com/Sch8ill/MCClient-lib").