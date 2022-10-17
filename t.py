



import socket
import struct
import time



from mcipc.query import Client

with Client('127.0.0.1', 25565) as client:
    basic_stats = client.stats()            # Get basic stats.
    full_stats = client.stats(full=True)    # Get full stats.

print(basic_stats)
print(full_stats)