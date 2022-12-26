import datetime


class Players:
    def __init__(self, online, max, list):
        self.online = online
        self.max = max
        self.list = list


class Version:
    def __init__(self, name, protocol):
        self.name = name
        self.protocol = protocol


class StatusResponse:
    def __init__(self, host, port, raw_res):
        self.host = host
        self.port = port
        self.raw_res = raw_res
        self.res = {}

        self.res["host"] = self.host
        self.res["port"] = port


    @staticmethod
    def _remove_color_codes(cstr):
        color_codes = ["a", "b", "c", "d", "e", "f", "k", "l", "m", "n", "o", "r", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for code in color_codes:
            cstr = cstr.replace("§" + code, "")
        return cstr



class SLPResponse(StatusResponse):
    def __init__(self, host, port, raw_res):
        super().__init__(host, port, raw_res)

        self.res = self._parse_slp_res(self.raw_res)
        self.motd = self.res["motd"]
        self.version = Version(self.res["version"]["name"], self.res["version"]["protocol"])
        self.players = Players(self.res["players"]["online"], self.res["players"]["max"], self.res["players"]["list"])
        self.timestamp = str(datetime.datetime.now())


    def _parse_slp_res(self, slp_res):
        slp_res = self._add_missing(slp_res)

        if "sample" in slp_res["players"]:
            slp_res["players"]["list"] = slp_res["players"]["sample"]
            slp_res["players"].pop("sample")

        if "description" in slp_res:
            slp_res["motd"] = slp_res["description"]
            slp_res.pop("description")

        else:
            slp_res["motd"] = ""

        for player in slp_res["players"]["list"]:
            player["last_seen"] = str(datetime.datetime.now())

        if "favicon" in slp_res:
            slp_res.pop("favicon")

        slp_res["motd"] = self._parse_motd(slp_res["motd"])
        slp_res["version"]["name"] = self._remove_color_codes(slp_res["version"]["name"])
        slp_res["status"] = "online"
        return slp_res


    @classmethod
    def _parse_motd(cls, raw_motd):
        motd = ""
        if type(raw_motd) == dict:
            entries = raw_motd.get("extra", [])
            end = raw_motd.get("text", "")

            for entry in entries:
                motd += entry.get("text", "")
            motd += end

        elif type(raw_motd) == str:
            motd = raw_motd

        motd = motd.replace("\n", " ").strip()
        motd = cls._remove_color_codes(motd)
        return motd


    @staticmethod
    def _add_missing(res):
        default_res = {
            "previewsChat": None,
            "enforcesSecureChat": None,
            "description": "",
            "version": {"name": "", "protocol": -1},
            "players": {"online": -1, "max": -1, "list":[]}
        }

        for key in default_res:
            if key not in res:
                res[key] = default_res[key]

        res["players"]["list"] = default_res["players"]["list"]
        return res



class SLPLegacyResponse(StatusResponse):
    def __init__(self, host, port, raw_res):
        super().__init__(host, port, raw_res)

        self.res = self._parse_res(self.raw_res)
        self.motd = self.res["motd"]
        self.version = Version(self.res["version"], None)
        self.players = Players(self.res["online"], self.res["max"], None)


    @staticmethod
    def _parse_res(raw_res):
        res = {}
        res["version"] = raw_res[2]
        res["motd"] = raw_res[3]
        res["online"] = raw_res[4]
        res["max"] = raw_res[5]
        return res



class QueryResponse(StatusResponse):
    def __init__(self, host, port, raw_res):
        super().__init__(host, port, raw_res)

        self.res = raw_res

        self.motd = self.res["motd"]
        self.gametype = self.res["gametype"]
        self.game_id = self.res["game_id"]
        self.plugins = self.res["plugins"]
        self.map = self.res["map"]
        self.hostip = self.res["hostip"]
        self.hostport = self.res["hostport"]

        self.players = Players(self.res["numplayers"], self.res["maxplayers"], self.res["players"])
        self.version = Version(self.res["version"], None)
        self.version.software = self.res["software"]



class BedrockResponse(StatusResponse):
    def __init__(self, host, port, raw_res):
        super().__init__(host, port, raw_res)

        self.res = {}
        self.res["brand"] = self.raw_res[0]
        self.res["motd"] = self.raw_res[1]
        self.res["protocol"] = int(self.raw_res[2])
        self.res["version"] = self.raw_res[3]
        self.res["online_players"] = int(self.raw_res[4])
        self.res["max_players"] = int(self.raw_res[5])
        self.res["server_id"] = self.raw_res[6]

        self.res["map"] = None
        self.res["gametype"] = None
        if len(self.raw_res) > 6:
            self.res["map"] = self.raw_res[7]

        if len(self.raw_res) > 7:
            self.res["gametype"] = self.raw_res[8]

        self.brand = self.res["brand"]
        self.motd = self.res["motd"]
        self.protocol = self.res["protocol"]
        self.version = self.res["version"]
        self.online_players = self.res["online_players"]
        self.max_players = self.res["max_players"]
        self.server_id = self.res["server_id"]
        self.map = self.res["map"]
        self.gametype = self.res["gametype"]
