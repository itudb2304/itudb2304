from models.constituent import Constituent
from models.constituent_objects import ConstituentObjects

class ConstituentRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_all_constituents(self):
        try:
            constituents = []
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM constituents LIMIT 500;"
                cursor.execute(query)
                constituents = cursor.fetchall()
                constituents = [Constituent(x) for x in constituents]
            self.connection.commit()
            return constituents
        except Exception as e:
            print(f"Error getting all constituents from the database: {e}")
            self.connection.rollback()


    def get_constituent_by_id(self, id: int):
        try:
            constituents = []
            with self.connection.cursor() as cursor:
                query = f"SELECT * FROM constituents WHERE constituentid={id};"
                cursor.execute(query)
                constituents = cursor.fetchall()
                constituents = [Constituent(x) for x in constituents]
            self.connection.commit()
            return constituents[0]
        except Exception as e:
            print(f"Error getting constituent by id from the database: {e}")
            self.connection.rollback()
            
    def get_constituents_by_name(self, name):
        try:
            constituents = []
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM constituents c WHERE c.forwarddisplayname LIKE %s;"
                cursor.execute(query, ('%' + name + '%', ))
                constituents = cursor.fetchall()
                constituents = [Constituent(x) for x in constituents]
            self.connection.commit()
            return constituents
        except Exception as e:
            print(f"Error getting constituent by name from the database: {e}")
            self.connection.rollback()
    
    def add_constituent(self, attributes: list):
        try:
            constituent = Constituent(attributes=attributes)
            with self.connection.cursor() as cursor:
                query = '''INSERT INTO constituents (
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
                                    constituenttype, 
                                    wikidataid
                                    ) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                cursor.execute(query, (constituent.ulanid,
                                            constituent.preferreddisplayname,
                                            constituent.forwarddisplayname,
                                            constituent.lastname,
                                            constituent.displaydate,
                                            constituent.artistofngaobject,
                                            constituent.beginyear,
                                            constituent.endyear,
                                            constituent.visualbrowsertimespan,
                                            constituent.nationality,
                                            constituent.constituenttype,
                                            constituent.wikidataid))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error inserting constituent to the database: {e}")
            self.connection.rollback()
    
    def constituent_objects(self, constituentid: int):
        try:
            objects_info = []
            with self.connection.cursor() as cursor:
                query = '''SELECT DISTINCT oc.id, oc.objectID, oc.constituentID, oc.roleType,
                oc.role, oc.displayDate, oc.displayOrder, oc.country, o.title, c.forwarddisplayname 
                FROM constituents c
                LEFT JOIN objects_constituents oc on c.constituentid = oc.constituentID
                LEFT JOIN objects o on o.objectid = oc.objectID
                WHERE c.constituentid = %s;
                ;
                '''
                cursor.execute(query, (constituentid,))
                objects_info = cursor.fetchall()
                objects_info = [ConstituentObjects(i) for i in objects_info]
                self.connection.commit()
                return objects_info
        except Exception as e:
            print(f"Error getting constituent objects from the database: {e}")
            self.connection.rollback()
        
    def add_constituent_object(self, attributes: list):
        try:
            with self.connection.cursor() as cursor:
                query = '''INSERT INTO objects_constituents (
                                    objectID,
                                    constituentID,
                                    roleType,
                                    role,
                                    displayDate,
                                    displayOrder,
                                    country
                                    )
                                    VALUES (%s, %s, %s, %s, %s, %s, %s);'''
                cursor.execute(query, (attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], attributes[5], attributes[6]))
            self.connection.commit()
        except Exception as e:
            print(f"Error inserting constituent object to the database: {e}")
            self.connection.rollback()

    def get_constituent_object_by_id(self, id: int):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                SELECT DISTINCT oc.id, oc.objectID, oc.constituentID, oc.roleType,
                oc.role, oc.displayDate, oc.displayOrder, oc.country, o.title, c.forwarddisplayname 
                FROM constituents c
                LEFT JOIN objects_constituents oc on c.constituentid = oc.constituentID
                LEFT JOIN objects o on o.objectid = oc.objectID
                WHERE oc.id = %s;
                '''
                cursor.execute(query, (id,))
                constituent_object = (cursor.fetchall())[0]
                constituent_object = ConstituentObjects(constituent_object)
                return constituent_object
        except Exception as e:
            print(f"Error getting constituent object by id from the database: {e}")
            self.connection.rollback()

    # TODO: later move this function to objects repository
    # TODO: remove limit
    def get_object_ids(self):
        try:
            object_ids = []
            with self.connection.cursor() as cursor:
                query = '''SELECT objectid FROM objects LIMIT 10;'''
                cursor.execute(query)
                object_ids = cursor.fetchall()
            self.connection.commit()
            return object_ids
        except Exception as e:
            print(f"Error getting object ids from the database: {e}")
            self.connection.rollback()
    
    # TODO: remove limit
    def get_constituent_ids(self):
        try:
            constituent_ids = []
            with self.connection.cursor() as cursor:
                query = '''SELECT constituentid FROM constituents LIMIT 10;'''
                cursor.execute(query)
                constituent_ids = cursor.fetchall()
            return constituent_ids
        except Exception as e:
            print(f"Error getting constituent ids from the database: {e}")
            self.connection.rollback()
    
    def update_constituent_object(self, attributes: list, relationid: int):
        try:
            with self.connection.cursor() as cursor:
                query = '''UPDATE objects_constituents SET
                                    roleType = %s,
                                    role = %s,
                                    displayDate = %s,
                                    displayOrder = %s,
                                    country = %s
                                    WHERE id = %s;'''
                cursor.execute(query, (attributes[2], attributes[3], attributes[4], attributes[5], attributes[6], relationid))
            self.connection.commit()
        except Exception as e:
            print(f"Error updating constituent object in the database: {e}")
            self.connection.rollback()

    def delete_constituent_object(self, relationid: int):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                DELETE FROM objects_constituents
                WHERE id=%s;
                '''
                cursor.execute(query, (relationid,))
                self.connection.commit()
        except Exception as e:
            print(f"Error deleting constituent object from the database: {e}")
            self.connection.rollback()
