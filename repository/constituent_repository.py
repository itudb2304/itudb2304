from models.constituent import Constituent

class ConstituentRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_all_constituents(self):
        constituents = []
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM constituents LIMIT 500;"
            cursor.execute(query)
            constituents = cursor.fetchall()
            constituents = [Constituent(x) for x in constituents]
        self.connection.commit()
        return constituents

    def get_constituent_by_id(self, id: int):
        constituents = []
        with self.connection.cursor() as cursor:
            query = f"SELECT * FROM constituents WHERE constituentid={id};"
            cursor.execute(query)
            constituents = cursor.fetchall()
            constituents = [Constituent(x) for x in constituents]
        self.connection.commit()
        return constituents[0]
            
    def get_constituents_by_name(self, name):
        constituents = []
        with self.connection.cursor() as cursor:
            query = f"SELECT * FROM constituents c WHERE c.forwarddisplayname LIKE '%{name}%';"
            cursor.execute(query)
            constituents = cursor.fetchall()
            constituents = [Constituent(x) for x in constituents]
        self.connection.commit()
        return constituents
    
    def add_constituent(self, attributes: list):
        constituent = Constituent(attributes=attributes)
        with self.connection.cursor() as cursor:
            query = '''INSERT INTO constituents (
                                constituentid, 
                                ulanid, 
                                preferreddisplayname, 
                                forwarddisplayname, 
                                lastname, 
                                displaydate, 
                                artistofngaobject, 
                                beginyear, 
                                endyear, 
                                visualbrowsertimespan, 
                                nationality, 
                                visualbrowsernationality, 
                                constituenttype, 
                                wikidataid
                                ) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
            cursor.execute(query, (constituent.constituentid,
                                        constituent.ulanid,
                                        constituent.preferreddisplayname,
                                        constituent.forwarddisplayname,
                                        constituent.lastname,
                                        constituent.displaydate,
                                        constituent.artistofngaobject,
                                        constituent.beginyear,
                                        constituent.endyear,
                                        constituent.visualbrowsertimespan,
                                        constituent.nationality,
                                        constituent.visualbrowsernationality,
                                        constituent.constituenttype,
                                        constituent.wikidataid))
        self.connection.commit()
        return constituent.constituentid
    
    def constituent_objects(self, constituentid: int):
        objects = []

        
