from mcclient.address import Address


def test_address():
    test_domain = Address("google.com").get_host()
    # add more tests for test_domain

    test_ip = Address("23.23.23.23").get_host()
    assert test_ip[0] == "23.23.23.23"

    test_srv_record = Address("pokecentral.org").get_host() # random server for testing, needs to be changed!
    assert test_srv_record[1] == 25565