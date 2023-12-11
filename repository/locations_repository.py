class Location:
<<<<<<< HEAD
    def __init__(self, name, type, isPublic = None, partof = None, key = None ) -> None:
        self.name = name
        self.key = key
        self.type = type
        self.isPublic = isPublic
        self.building = None
        self.floor = None
        self.partof = partof
=======
    def __init__(self, name, objects) -> None:
        self.name = name
        self.objects = objects
>>>>>>> 83da0908d6825cdbb0fe57603761abe5324fb136

class LocationsRepository:
    def __init__(self, connection) -> None:
        self.connection = connection
        
    def get_buildings(self):
        buildings = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT DISTINCT p.description, p.locationkey FROM preferred_locations AS p
<<<<<<< HEAD
=======
                JOIN locations AS l
                ON l.site = p.description 
>>>>>>> 83da0908d6825cdbb0fe57603761abe5324fb136
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
    
<<<<<<< HEAD
    def get_objects(self, room_id):
=======
    def get_room(self, room_id):
>>>>>>> 83da0908d6825cdbb0fe57603761abe5324fb136
        objects = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT p.description FROM preferred_locations AS p
                WHERE p.locationkey = %s;
            '''
            cursor.execute(query, [room_id])
            room_name = cursor.fetchone()
            query = '''
                SELECT o.objectid FROM objects AS o
                WHERE o.locationid = %s;
            '''
            cursor.execute(query, [room_id])
            for object_id in cursor:
                objects.append((object_id))
<<<<<<< HEAD
        return objects
=======
        room = Location(room_name, objects)
        return room
>>>>>>> 83da0908d6825cdbb0fe57603761abe5324fb136
    
    def get_locationkey(self, location_id):
        locationkey = ""
        with self.connection.cursor() as cursor:
            query = ''' 
                SELECT l.room FROM locations AS l
                WHERE l.locationid = %s; '''
            cursor.execute(query, [location_id])
            for key in cursor:
                locationkey = key
<<<<<<< HEAD
        return locationkey
    
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
        print(location.key)
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

    def get_location(self, locationkey):
        with self.connection.cursor() as cursor:
            query = '''
                SELECT description, locationtype, ispublicvenue, partof FROM preferred_locations as p
                WHERE p.locationkey = %s;
            '''
            cursor.execute(query, [locationkey])
            name, type, isPublic, partof = cursor.fetchone()
        return Location(key =locationkey, name= name, type= type, isPublic=isPublic, partof=partof)
=======
        return locationkey
>>>>>>> 83da0908d6825cdbb0fe57603761abe5324fb136
