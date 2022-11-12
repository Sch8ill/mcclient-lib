from mcstatus import JavaServer

# You can pass the same address you'd enter into the address field in minecraft into the 'lookup' function
# If you know the host and port, you may skip this and use JavaServer("example.org", 1234)
server = JavaServer.lookup("185.14.95.45:29565")


q = server.query()
print(q.raw)
