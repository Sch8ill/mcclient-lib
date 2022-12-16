
from client import MCClient

class Player:
    name = "testbot69"

player = Player()



c = MCClient(host="mc.internetpolice.ga", port=29565, version=761)
c.connect()
c.login(player)