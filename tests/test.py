
from client import MCClient

class Player:
    name = "testbot69"

player = Player()



c = MCClient(version=761)
c.connect()
c.login(player)