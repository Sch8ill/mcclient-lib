# Documentation for MCClient

## Response fields
| field                   | Basic SLP | Legacy SLP | Query | Bedrock SLP | Usage                |
| ----------------------- | --------- | ---------- | ----- | ----------- | -------------------- |
| motd                    | yes       | yes        | yes   | yes         | res.motd             |
| online player count     | yes       | yes        | yes   | yes         | res.players.online   |
| max players             | yes       | yes        | yes   | yes         | res.players.max      |
| player list             | depends   | no         | yes   | no          | res.players.list     |
| server version          | yes       | yes        | yes   | yes         | res.version.name     |
| server protocol version | yes       | no         | yes   | no          | res.version.protocol |
| mods and plugins        | depends   | no         | yes   | no          |                      |
| has favicon             | yes       | no         | no    | no          | res.favicon          |
| gametype                | no        | no         | yes   | depends     | res.gametype         |
| name of map             | no        | no         | yes   | depends     | res.map              |