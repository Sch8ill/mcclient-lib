from mcclient.address import Address

print(Address("mcraspi.com").get_host())
print(Address("mc.internetpolice.ga").get_host())
print(Address("23.23.23.23").get_host())