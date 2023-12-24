class Location:
    def __init__(self, name, type, isPublic = None, partof = None, key = None, building = None ) -> None:
        self.name = name
        self.key = key
        self.type = type
        self.isPublic = isPublic
        self.building = building
        self.floor = None
        self.partof = partof

class LocationsRepository:
    def __init__(self, connection) -> None:
        self.connection = connection
        
    def get_locations(self, filter):
        try:
            with self.connection.cursor() as cursor:
                locations = []
                execution_list = []
                query = '''
                        SELECT DISTINCT l.description, p.locationtype, l.publicaccess, p.partof, p.locationkey, l.site
                        FROM locations AS l
                        LEFT JOIN preferred_locations AS p 
                        ON l.room = p.locationkey;'''    
                if filter:
                    filter ='%' + filter + '%'
                    execution_list.append(filter)
                    query = query[:-1] + " WHERE l.description LIKE %s;"
                    
                cursor.execute(query, execution_list)
 
                search_results = cursor.fetchall()
                for name, type, isPublic, partof, key, building in search_results:
                    locations.append(Location(name, type, isPublic, partof, key, building))
    
                return locations
        except Exception as e:
             print(f"Error getting locations from the database: {e}")
        
    def get_buildings(self):
        try:    
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
        except Exception as e:
             print(f"Error getting buildings from the database: {e}")
    
    def get_floors(self, building_id):
        try:
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
        except Exception as e:
            print(f"Error getting floors from the database: {e}")
    
    def get_rooms(self, floor_id):
        try:
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
        except Exception as e:
            print(f"Error getting rooms from the database: {e}")

    def get_objects(self, room_id):
        try:
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
        except Exception as e:
            print(f"Error getting objects of the location from the database: {e}")
    
    def get_locationkey(self, location_id):
        try:
            locationkey = ""
            with self.connection.cursor() as cursor:
                query = ''' 
                    SELECT l.room FROM locations AS l
                    WHERE l.locationid = %s; '''
                cursor.execute(query, [location_id])
                for key in cursor:
                    locationkey = key
            return locationkey
        except Exception as e:
            print(f"Error getting locationkey from the database: {e}")

    def get_locationid(self, locationkey):
        try:
            locationid = ""
            with self.connection.cursor() as cursor:
                query = ''' 
                    SELECT l.locationid FROM locations AS l
                    WHERE l.room = %s; '''
                cursor.execute(query, [locationkey])
                for id in cursor:
                    locationid = id
            return locationid
        except Exception as e:
            print(f"Error getting locationid from the database: {e}")
    
    def is_locationkey_unique(self, location_key):
        try:
            with self.connection.cursor() as cursor:
                query = '''SELECT locationkey FROM preferred_locations WHERE locationkey = %s;'''
                cursor.execute(query, [location_key])
                row = None
                for key in cursor:
                    row = key
            return row is None
        except Exception as e:
            print(f"Error controlling locationkey: {e}")

    def is_name_unique(self, location_name):
        try:
            with self.connection.cursor() as cursor:
                query = '''SELECT locationkey FROM preferred_locations WHERE description = %s;'''
                cursor.execute(query, [location_name])
                row = None
                for key in cursor:
                    row = key
            return row is None
        except Exception as e:
            print(f"Error controlling name: {e}")

    def create_locationkey(self, location):
        try:
            key = '-'.join(word[0] for word in location.name.split())
            locationkey = key
            count = 1
            while not self.is_locationkey_unique(locationkey):
                locationkey = f"{key}{count}"
                count += 1
            location.key = locationkey
            return locationkey
        except Exception as e:
            print(f"Error creating locationkey: {e}")

    def add_location(self, new_location):
        try:
            locationkey = self.create_locationkey(new_location)
            with self.connection.cursor() as cursor:
                query = '''INSERT INTO preferred_locations (locationkey, locationtype, description, ispublicvenue, partof)
                        VALUES(%s, %s, %s, %s, %s);'''
                cursor.execute(query, (new_location.key, new_location.type, new_location.name, new_location.isPublic, new_location.partof))
                self.connection.commit()
            return locationkey
        except Exception as e:
            print(f"Error adding location to the database: {e}")
    
    def update_location(self, location):
        try:
            with self.connection.cursor() as cursor:
                query = '''UPDATE preferred_locations SET locationtype = %s, description = %s, ispublicvenue = %s, partof = %s
                        WHERE locationkey = %s;'''
                cursor.execute(query, (location.type, location.name, location.isPublic, location.partof, location.key))
                self.connection.commit()
        except Exception as e:
            print(f"Error updating location from the database: {e}")

    def delete_location(self, location):
        try:
            with self.connection.cursor() as cursor:
                if location.type == "room":
                    self.delete_locationid(location.key)
                else:
                    query = '''SELECT locationkey FROM preferred_locations WHERE partof= %s;'''
                    cursor.execute(query, [location.key])
                    sublocations = cursor.fetchall()
                    for sublocation in sublocations:
                        self.delete_location(sublocation[0])
                query = '''DELETE FROM preferred_locations WHERE locationkey = %s;'''
                cursor.execute(query, [location.key])
                self.connection.commit()

        except Exception as e:
            print(f"Error deleting location from the database: {e}")

    def get_location(self, locationkey):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                    SELECT description, locationtype, ispublicvenue, partof FROM preferred_locations as p
                    WHERE p.locationkey = %s;
                '''
                cursor.execute(query, [locationkey])
                name, type, isPublic, partof = cursor.fetchone()
            return Location(key =locationkey, name= name, type= type, isPublic=isPublic, partof=partof)
        except Exception as e:
            print(f"Error getting location from the database: {e}")

    def add_locationid(self, location):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                    SELECT MAX(locationid) FROM locations;
                '''
                cursor.execute(query)
                max_id= cursor.fetchone()
                location_id = max_id[0] + 1            
                query = '''INSERT INTO locations (locationid, site, room, publicaccess, description)
                        VALUES(%s, %s, %s, %s, %s);'''
                cursor.execute(query, (location_id, location.building, location.key, location.isPublic, location.name))
                self.connection.commit()
        except Exception as e:
            print(f"Error adding locationid to the database: {e}")

    def update_locationid(self, location):
        try:
            with self.connection.cursor() as cursor:           
                query = '''UPDATE locations SET publicaccess = %s, description = %s
                    WHERE locationid IN (SELECT locationid FROM (SELECT l.locationid FROM locations AS l WHERE l.room = %s)AS subquery);'''
                cursor.execute(query, (location.isPublic, location.name, location.key))
                self.connection.commit()
        except Exception as e:
            print(f"Error updating locationid from the database: {e}")
        
    def delete_locationid(self, locationkey):
        try:
            with self.connection.cursor() as cursor:
                query = '''DELETE FROM locations WHERE room = %s;'''
                cursor.execute(query, [locationkey])
                self.connection.commit()
        except Exception as e:
            print(f"Error deleting locationid from the database: {e}")

    def add_object(self, object_id, locationkey):
        try:
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
        except Exception as e:
            print(f"Error adding object to a location: {e}")

    def remove_object(self, object_id):
        try:
            with self.connection.cursor() as cursor:
                query = ''' UPDATE objects SET locationid = NULL WHERE objectid = %s;'''
                cursor.execute(query, (object_id,))
                self.connection.commit()
        except Exception as e:
            print(f"Error removing object from a location: {e}")