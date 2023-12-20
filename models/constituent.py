class Constituent:
    def __init__(
        self,
        attributes: list
    ):
        if len(attributes) == 14:
            self.constituentid = attributes[0] # NOT NULL
            self.ulanid = attributes[1]
            self.preferreddisplayname = attributes[2]
            self.forwarddisplayname = attributes[3]
            self.lastname = attributes[4]
            self.displaydate = attributes[5]
            self.artistofngaobject = attributes[6] # NOT NULL
            self.beginyear = attributes[7]
            self.endyear = attributes[8]
            self.visualbrowsertimespan = attributes[9]
            self.nationality = attributes[10] 
            self.visualbrowsernationality = attributes[11]
            self.constituenttype = attributes[12] # NOT NULL
            self.wikidataid = attributes[13] 
        else:
            self.ulanid = attributes[0]
            self.preferreddisplayname = attributes[1]
            self.forwarddisplayname = attributes[2]
            self.lastname = attributes[3]
            self.displaydate = attributes[4]
            self.artistofngaobject = attributes[5] # NOT NULL
            self.beginyear = attributes[6]
            self.endyear = attributes[7]
            self.visualbrowsertimespan = attributes[8] 
            self.nationality = attributes[9] 
            self.constituenttype = attributes[10] # NOT NULL
            self.wikidataid = attributes[11] 
