# MCClient
A lightweight Minecraft client to query the status of a Minecraft server.

### Supported Mincraft versions
* Minecraft Java (1.7.* -> 1.19.*)
*  Minecraft Bedrock

### Supported protocols
* Basic ServerListPing
* Legacy ServerListPing
* Query Protocol (Full stat)
* Bedrock ServerListPing

## Installation
### pypi
```bash
pip install mcclient-lib
```

## Usage
### Basic ServerListPing
```python
from mcclient import SLPClient

slp_client = SLPClient("mc.example.com", port=12345)
res = slp_client.get_status()
print(res.motd)
 ```
### Query
```python
from mcclient import QueryClient

query_client = QueryClient(mc.example.com, port=12345)
res = query_client.get_status()
print(res.motd)
```

### Bedrock ServerListPing
```python
from mcclient import BedrockSLPClient

bedrock_slp_client = BedrockSLPClient(mc.example.com, port=12345)
res = bedrock_slp_client.get_status()
print(res.motd)
```
## Queryable data
* motd (all)
* online player count (all)
* max player count (all)
* player list (basic ServerListPing and query slp)
* server version (all)
* server protocol version (Basic Serverlistping, query slp and Bedrock slp)
* mods and plugins (basic ServerListPing on Forge and query slp)
* has a favicon (basic ServerListPing)
* name of map (query slp)
* hostport and hostip (query slp)
* gametype (query slp and Bedrock slp)
* server id (Bedrock slp)

## Documentation
There is no real documentation, just look into the [source](https://github.com/Sch8ill/MCClient-lib "github.com/Sch8ill/MCClient-lib").