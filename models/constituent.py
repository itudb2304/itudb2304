class Constituent:
    def __init__(
        self,
        attributes: list
    ):
        self.constituentid = attributes[0]
        self.ulanid = attributes[1]
        self.preferreddisplayname = attributes[2]
        self.forwarddisplayname = attributes[3]
        self.lastname = attributes[4]
        self.displaydate = attributes[5]
        self.artistofngaobject = attributes[6]
        self.beginyear = attributes[7]
        self.endyear = attributes[8]
        self.visualbrowsertimespan = attributes[9]
        self.nationality = attributes[10] 
        self.visualbrowsernationality = attributes[11]
        self.constituenttype = attributes[12] 
        self.wikidataid = attributes[13] 
