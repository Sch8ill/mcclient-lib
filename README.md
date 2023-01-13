# MCClient
A lightweight Minecraft client to query a Minecraft servers status.

### Supported Mincraft versions
* Minecraft Java (1.7.* -> 1.19.*)
*  Minecraft Bedrock

### Supported protocols
* Basic ServerListPing
* Legacy ServerListPing
* Query Protocol (Full stat)
* Bedrock ServerListPing

## Installation 
### local
```
git clone https://github.com/Sch8ill/MCClient
```
```
pip install .
```
### pypi
```
pip install mcclient
```
IMPORTANT: There is no pypi package yet.


## Usage
### Basic ServerListPing
```
from mcclient import SLPClient

slp_client = SLPClient("mc.example.com", port=12345)
res = slp_client.get_status()
print(res.motd)
 ```
### Query
```
from mcclient import QueryClient

query_client = QueryClient(mc.example.com, port=12345)
res = query_client.get_status()
print(res.motd)
```

### Bedrock ServerListPing
```
from mcclient import BedrockSLPClient

bedrock_slp_client = BedrockSLPClient(mc.example.com, port=12345)
res = bedrock_slp_client.get_status()
print(res.motd)
