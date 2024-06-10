from mcclient.address import Address


def test_address():
    # random addresses for testing

    assert Address("google.com", 0).get_host() == "google.com"
    # add more tests for test_domain

    assert Address("23.23.23.23", 0).get_host() == "23.23.23.23"

    # random addresses for testing
    addr = Address("hypixel.net", 0)
    addr.resolve()
    assert addr.address() == ("mc.hypixel.net", 25565)
