# Documentation for MCClient

## Response fields
| field                   | SLP     | Legacy SLP | Query | Bedrock SLP | Usage                    |
| ----------------------- | ------- | ---------- | ----- | ----------- | ------------------------ |
| motd                    | yes     | yes        | yes   | yes         | res.motd                 |
| online player count     | yes     | yes        | yes   | yes         | res.players.online       |
| max players             | yes     | yes        | yes   | yes         | res.players.max          |
| player list             | depends | no         | yes   | no          | res.players.list         |
| server version          | yes     | yes        | yes   | yes         | res.version.name         |
| server protocol version | yes     | no         | yes   | yes         | res.version.protocol     |
| mods and plugins        | depends | no         | yes   | no          | res.plugins              |
| has favicon             | yes     | no         | no    | no          | res.favicon              |
| gametype                | no      | no         | yes   | depends     | res.gametype             |
| name of map             | no      | no         | yes   | depends     | res.map                  |
| server id               | no      | no         | no    | yes         | res.server_id            |
| host port and ip        | no      | no         | yes   | no          | res.hostport, res.hostip |
| timestamp               | yes     | yes        | yes   | yes         | res.timstamp             |
| response as dictonary   | yes     | yes        | yes   | yes         | res.res                  |


## Base client
You can also write your own client using the [BaseClient](https://github.com/Sch8ill/MCClient-lib/blob/master/mcclient/base_client.py "github.com/Sch8ill/MCClient-lib/mcclient/base_client.py") class as a foundation.
An example of this is this simple [login script](https://github.com/Sch8ill/MCClient-lib/blob/master/examples/login.py "github.com/Sch8ill/MCClient-lib/examples/login.py").


## Scanning
This client is very usefull for scanning since it allows alredy connected sockets to be implanted into the client.
Here is an example:
```python
from mcclient import SLPClient

def mc_check(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port)) # The socket thats going to be implanted has to be connected
        slp_client = SLPClient(host=ip, port=port)
        slp_client.implant_socket(sock)
        res = slp_client.get_status()

    except Except as e:
        ...
```

This also works with the LegacySLPClient or every other client that is based on the [BaseClient](https://github.com/Sch8ill/MCClient-lib/blob/master/docs.md#Base-client "baseClient")