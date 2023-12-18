from models.constituent import Constituent

class ConstituentRepository:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_all_constituents(self):
        constituents = []
        query = "SELECT * FROM constituents LIMIT 500;"
        self.cursor.execute(query)
        constituents = self.cursor.fetchall()
        constituents = [Constituent(x) for x in constituents]
        return constituents

    def get_constituent_by_id(self, id: int):
        constituents = []
        query = f"SELECT * FROM constituents WHERE constituentid={id};"
        self.cursor.execute(query)
        constituents = self.cursor.fetchall()
        constituents = [Constituent(x) for x in constituents]
        return constituents[0]
            
    def get_constituents_by_name(self, name):
        constituents = []
        if (len(name) == 0):
            return self.get_all_constituents()
        query = f"SELECT * FROM constituents c WHERE c.forwarddisplayname LIKE '%{name}%';"
        self.cursor.execute(query)
        constituents = self.cursor.fetchall()
        constituents = [Constituent(x) for x in constituents]
        return constituents
