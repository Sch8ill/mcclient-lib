from mcclient.response import StatusResponse


def test_remove_color_codes():
    tests = [
        # basic tests
        ("§cHello §lworld§r!", False, "Hello world!"),
        ("§eHello §kworld§r!", True, "Hello world!"),
        ("Hello world!", False, "Hello world!"),

        # Tests with repeated color codes
        ("§c§cRed§r", False, "Red"),
        ("§e§eYellow§r", True, "Yellow"),

        # Tests with invalid color codes
        ("§xHello§y", False, "§xHello§y"),

        # Tests with different formatting codes
        ("§fHello §oWorld§r", False, "Hello World"),
        ("§fHello §oWorld§r", True, "Hello World"),

        # Tests with mixed formatting and color codes
        ("§e§lHello §c§oWorld§r", False, "Hello World"),
        ("§e§lHello §c§oWorld§r", True, "Hello World")
    ]

    test_res = StatusResponse("", 0, {})

    for cstr, bedrock, expected_output in tests:
        assert test_res._remove_color_codes(cstr, bedrock) == expected_output
