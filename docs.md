# Documentation for MCClient

## Response fields

| field                   | SLP     | Legacy SLP | Query | Bedrock | Usage                    |
| ----------------------- | ------- | ---------- | ----- | ------- | ------------------------ |
| motd                    | yes     | yes        | yes   | yes     | res.motd                 |
| online player count     | yes     | yes        | yes   | yes     | res.players.online       |
| max players             | yes     | yes        | yes   | yes     | res.players.max          |
| player list             | depends | no         | yes   | no      | res.players.list         |
| server version          | yes     | yes        | yes   | yes     | res.version.name         |
| server protocol version | yes     | no         | yes   | yes     | res.version.protocol     |
| mods and plugins        | depends | no         | yes   | no      | res.plugins              |
| has favicon             | yes     | no         | no    | no      | res.favicon              |
| gametype                | no      | no         | yes   | depends | res.gametype             |
| name of map             | no      | no         | yes   | depends | res.map                  |
| server id               | no      | no         | no    | yes     | res.server_id            |
| host port and ip        | no      | no         | yes   | no      | res.hostport, res.hostip |
| timestamp               | yes     | yes        | yes   | yes     | res.timstamp             |
| response as dictonary   | yes     | yes        | yes   | yes     | res.res                  |

## Base client

You can also write your own client using the [BaseClient](https://github.com/Sch8ill/MCClient-lib/blob/master/mcclient/base_client.py "github.com/Sch8ill/MCClient-lib/mcclient/base_client.py") class as a foundation.

## Scanning

This client is very usefull for scanning since it allows alredy connected sockets to be implanted into the client.
Here is an example:

```python
from mcclient import SLPClient

def mc_check(sock, ip, port):
    try:
        # initiate the client
        # srv=False disables srv lookups, this can improve performance when only connecting to ip's/domain's without srv records.
        slp_client = SLPClient(host=ip, port=port, srv=False)
        # implant the already connected socket
        slp_client.implant_socket(sock)
        # retreive the status data
        res = slp_client.get_status()

    except Exception as e:
        ...
```

This also works with the LegacySLPClient or every other client that is based on the [BaseClient](https://github.com/Sch8ill/MCClient-lib/blob/master/docs.md#Base-client "baseClient")
