class Location:
    def __init__(self, name, type, isPublic = None, partof = None, key = None ) -> None:
        self.name = name
        self.key = key
        self.type = type
        self.isPublic = isPublic
        self.building = None
        self.floor = None
        self.partof = partof

class LocationsRepository:
    def __init__(self, connection) -> None:
        self.connection = connection
        
    def get_buildings(self):
        buildings = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT DISTINCT p.description, p.locationkey FROM preferred_locations AS p
                WHERE p.locationtype = "building";'''
            cursor.execute(query)
            for building, id in cursor:
                buildings.append([building, id])
        for building in buildings:
            building.append(self.get_floors(building[1]))
        return buildings
    
    def get_floors(self, building_id):
        floors = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT p.description, p.locationkey FROM preferred_locations as p
                WHERE p.partof = %s;
            '''
            cursor.execute(query, [building_id])
            for description, floor_id in cursor:
                floors.append((description, floor_id))
        return floors
    
    def get_rooms(self, floor_id):
        rooms = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT p.description, p.locationkey FROM preferred_locations as p
                WHERE p.partof = %s;
            '''
            cursor.execute(query, [floor_id])
            for description, room_id in cursor:
                rooms.append((description, room_id))
        return rooms
    
    def get_objects(self, room_id):
        objects = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT l.locationid FROM locations AS l
                WHERE l.room = %s;
            '''
            cursor.execute(query, [room_id])
            locations = cursor.fetchall()
            for location in locations:
                query = '''
                    SELECT o.objectid FROM objects AS o
                    WHERE o.locationid = %s;
                '''
                cursor.execute(query, [location[0]])
                for object_id in cursor:
                    objects.append((object_id))
        return objects
    
    def get_locationkey(self, location_id):
        locationkey = ""
        with self.connection.cursor() as cursor:
            query = ''' 
                SELECT l.room FROM locations AS l
                WHERE l.locationid = %s; '''
            cursor.execute(query, [location_id])
            for key in cursor:
                locationkey = key
        return locationkey
    
    def get_locationid(self, locationkey):
        locationid = ""
        with self.connection.cursor() as cursor:
            query = ''' 
                SELECT l.locationid FROM locations AS l
                WHERE l.room = %s; '''
            cursor.execute(query, [locationkey])
            for id in cursor:
                locationid = id
        return locationid
    
    def is_location_key_unique(self, location_key):
        with self.connection.cursor() as cursor:
            query = '''SELECT locationkey FROM preferred_locations WHERE locationkey = %s'''
            cursor.execute(query, [location_key])
            row = None
            for key in cursor:
                row = key
        return row is None
    
    def create_locationkey(self, location):
        key = '-'.join(word[0] for word in location.name.split())
        locationkey = key
        count = 1
        while not self.is_location_key_unique(locationkey):
            locationkey = f"{key}{count}"
            count += 1
        location.key = locationkey
        return locationkey

    def add_location(self, new_location):
        locationkey = self.create_locationkey(new_location)
        with self.connection.cursor() as cursor:
            query = '''INSERT INTO preferred_locations (locationkey, locationtype, description, ispublicvenue, partof)
                    VALUES(%s, %s, %s, %s, %s)'''
            cursor.execute(query, (new_location.key, new_location.type, new_location.name, new_location.isPublic, new_location.partof))
            self.connection.commit()
        return locationkey
    
    def update_location(self, location):
        with self.connection.cursor() as cursor:
            query = '''UPDATE preferred_locations SET locationtype = %s, description = %s, ispublicvenue = %s, partof = %s
                    WHERE locationkey = %s'''
            cursor.execute(query, (location.type, location.name, location.isPublic, location.partof, location.key))
            self.connection.commit()

    def delete_location(self, locationkey):
        with self.connection.cursor() as cursor:
            query = '''DELETE FROM preferred_locations WHERE locationkey = %s'''
            cursor.execute(query, [locationkey])
            self.connection.commit()
            query = '''SELECT locationkey FROM preferred_locations WHERE partof= %s'''
            cursor.execute(query, [locationkey])
            sublocations = cursor.fetchall()
            for sublocation in sublocations:
                self.delete_location(sublocation[0])

    def get_location(self, locationkey):
        with self.connection.cursor() as cursor:
            query = '''
                SELECT description, locationtype, ispublicvenue, partof FROM preferred_locations as p
                WHERE p.locationkey = %s;
            '''
            cursor.execute(query, [locationkey])
            name, type, isPublic, partof = cursor.fetchone()
        return Location(key =locationkey, name= name, type= type, isPublic=isPublic, partof=partof)

    def add_locationid(self, location):
        with self.connection.cursor() as cursor:
            query = '''
                SELECT MAX(locationid) FROM locations;
            '''
            cursor.execute(query)
            max_id= cursor.fetchone()
            location_id = max_id[0] + 1            
            query = '''INSERT INTO locations (locationid, site, room, publicaccess, description)
                    VALUES(%s, %s, %s, %s, %s)'''
            cursor.execute(query, (location_id, location.building, location.key, location.isPublic, location.name))
            self.connection.commit()

    def update_locationid(self, location):
        with self.connection.cursor() as cursor:           
            query = '''UPDATE locations SET publicaccess = %s, description = %s
                  WHERE locationid IN (SELECT locationid FROM (SELECT l.locationid FROM locations AS l WHERE l.room = %s)AS subquery);'''
            cursor.execute(query, (location.isPublic, location.name, location.key))
            self.connection.commit()
    
    def delete_locationid(self, locationkey):
        with self.connection.cursor() as cursor:
            query = '''DELETE FROM locations WHERE locationid IN (SELECT locationid FROM (SELECT l.locationid FROM locations AS l WHERE l.room = %s)AS subquery);'''
            cursor.execute(query, [locationkey])
            self.connection.commit()

    def add_object(self, object_id, locationkey):
        location_id = self.get_locationid(locationkey)
        with self.connection.cursor() as cursor:
            query = ''' SELECT * FROM objects WHERE objectid = %s; '''
            cursor.execute(query, (object_id,))
            isPresent = cursor.fetchall()
            if not isPresent:
                print("This object_id is not valid")
                return
            query = ''' UPDATE objects SET locationid = %s WHERE objectid = %s;'''

            cursor.execute(query, (location_id[0], object_id))
            self.connection.commit()

    def remove_object(self, object_id, locationkey):
        location_id = self.get_locationid(locationkey)
        with self.connection.cursor() as cursor:
            query = ''' UPDATE objects SET locationid = NULL WHERE objectid = %s;'''
            cursor.execute(query, (object_id,))
            self.connection.commit()