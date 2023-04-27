from mcclient.address import Address


def test_address():
    # random addresses for testing

    test_domain = Address("google.com").get_host()
    # add more tests for test_domain

    test_ip = Address("23.23.23.23").get_host()
    assert test_ip[0] == "23.23.23.23"

    # random addresses for testing
    test_srv_record = Address("pokecentral.org").get_host()
    assert test_srv_record[1] == 25565
