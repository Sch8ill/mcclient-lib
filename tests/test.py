
from mcclient.mcclient import MCClient

class Player:
    name = "testbot69"

player = Player()



c = MCClient()
c.connect()
c.login(player)