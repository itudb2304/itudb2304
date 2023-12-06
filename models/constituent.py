class Constituent:
    def __init__(
        self,
        attributes: list
    ):
        self.constituentid = attributes[0] if len(attributes) >= 0 else ""
        self.ulanid = attributes[1] if len(attributes) >= 1 else ""
        self.preferreddisplayname = attributes[2] if len(attributes) >= 2 else ""
        self.forwarddisplayname = attributes[3] if len(attributes) >= 3 else ""
        self.lastname = attributes[4] if len(attributes) >= 4 else ""
        self.displaydate = attributes[5] if len(attributes) >= 5 else ""
        self.artistofngaobject = attributes[6] if len(attributes) >= 6 else ""
        self.beginyear = attributes[7] if len(attributes) >= 7 else ""
        self.endyear = attributes[8] if len(attributes) >= 8 else ""
        self.visualbrowsertimespan = attributes[9] if len(attributes) >= 9 else ""
        self.nationality = attributes[10] if len(attributes) >= 10 else ""
        self.visualbrowsernationality = attributes[11] if len(attributes) >= 11 else ""
        self.constituenttype = attributes[12] if len(attributes) >= 12 else ""
        self.wikidataid = attributes[13] if len(attributes) >= 13 else ""
