class Location:
    def __init__(self, name, type, isPublic = None, partof = None, key = None, path = {"building": "", "floor": "", "room": ""} ) -> None:
        self.name = name
        self.key = key
        self.type = type
        self.isPublic = isPublic
        self.partof = partof
        self.path = path 
        self.shape = None
        self.coords = None
        

class LocationsRepository:
    def __init__(self, connection) -> None:
        self.connection = connection
        
    def get_locations(self, search, filter, limit = None, offset = None):
        try:
            with self.connection.cursor() as cursor:
                locations = []
                execution_list = []
                query = '''
                        SELECT * FROM (
                            SELECT DISTINCT
                                SUBSTRING_INDEX(SUBSTRING_INDEX(p.description, '/', -1),'-',-1) AS extracted_part,
                                p.locationtype AS type,
                                p.ispublicvenue AS public,
                                p.partof,
                                p.locationkey,
                                l.site
                            FROM
                                locations AS l
                            RIGHT JOIN
                                preferred_locations AS p ON l.room = p.locationkey
                        ) AS subquery;'''    

                if len(filter["type"]): 
                    query = query[:-1] + " WHERE type IN (" + ",".join(["%s"] * len(filter["type"])) + ");"
                    for type in filter["type"]:
                        execution_list.append(type) 
                elif not search and not len(filter["public"]):
                    query = query[:-1] + ''' WHERE type IN ("room");'''
                else:
                    query = query[:-1] + ''' WHERE type IN ("room", "floor", "building");'''

                if search:
                    search ='%' + search + '%'
                    execution_list.append(search)
                    query = query[:-1] + " AND extracted_part LIKE %s;"

                if len(filter["public"]):
                    execution_list.append(filter["public"][0])
                    query = query[:-1] + " AND public = %s;"

                query = query[:-1] + ''' ORDER BY CASE 
                                            WHEN type = 'building' THEN 1
                                            WHEN type= 'floor' THEN 2
                                            WHEN type = 'room' THEN 3
                                        END;'''
                
                if limit:
                    query = query[:-1] + " LIMIT %s;"
                    execution_list.append(limit)
                if offset:
                    query = query[:-1] + " OFFSET %s;"
                    execution_list.append(offset)
                cursor.execute(query, execution_list)
 
                search_results = cursor.fetchall()
                for name, type, isPublic, partof, key, building in search_results:
                    location = Location(name, type, isPublic, partof, key, path=self.get_path(key))
                    locations.append(location)
    
                return locations
        except Exception as e:
             print(f"Error getting locations from the database: {e}")
        
    def get_buildings(self):
        try:    
            buildings = []
            with self.connection.cursor() as cursor:
                query = '''
                    SELECT DISTINCT SUBSTRING_INDEX(SUBSTRING_INDEX(p.description, '/', -1),'-',-1), p.locationkey FROM preferred_locations AS p
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
                    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(p.description, '/', -1),'-',-1), p.locationkey FROM preferred_locations as p
                    WHERE p.partof = %s;
                '''
                cursor.execute(query, [building_id])
                for description, floor_id in cursor:
                    floors.append([description, floor_id])
                for floor in floors:
                    floor.append(self.get_rooms(floor[1]))
            return floors
        except Exception as e:
            print(f"Error getting floors from the database: {e}")
    
    def get_rooms(self, floor_id):
        try:
            rooms = []
            with self.connection.cursor() as cursor:
                query = '''
                    SELECT DISTINCT SUBSTRING_INDEX(SUBSTRING_INDEX(p.description, '/', -1),'-',-1), p.locationkey, p.locationtype,
                    p.mapshapetype, p.mapshapecoords FROM preferred_locations as p
                    LEFT JOIN locations as l ON p.locationkey = l.room
                    WHERE p.partof = %s;
                '''
                cursor.execute(query, [floor_id])
                for description, room_id, type, shape, coords in cursor:
                    room = Location(name = description, key= room_id, type= type )
                    room.shape = shape
                    room.coords = coords
                    rooms.append(room)
                    
            return rooms
        except Exception as e:
            print(f"Error getting rooms from the database: {e}")

    def get_objects(self, room_id):
        try:
            objects = []
            with self.connection.cursor() as cursor:
                query = '''
                    SELECT o.objectid FROM objects AS o
                    WHERE o.locationid IN (
                        SELECT l.locationid FROM locations AS l
                        WHERE l.room = %s
                    );
                '''
                cursor.execute(query, [room_id])
                for object_id in cursor:
                    objects.append(object_id)
            return objects
        except Exception as e:
            print(f"Error getting objects of the location from the database: {e}")
    
    def get_all_objects(self, locationkey):
        try:
            objects = []
            with self.connection.cursor() as cursor:
                sub = self.get_location(locationkey) 
                
                if sub.type == "room":
                    return self.get_objects(locationkey)      
                query = '''SELECT locationkey FROM preferred_locations WHERE partof= %s;'''
                cursor.execute(query, [locationkey])
                locations = cursor.fetchall()
                for location in locations:
                    objects.extend(self.get_all_objects(location[0]))
                return objects
        except Exception as e:
            print(f"Error getting all objects of the location from the database: {e}")
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

    def is_name_unique(self, location_name, locationkey):
        try:
            with self.connection.cursor() as cursor:
                query = '''SELECT locationkey FROM preferred_locations WHERE description = %s;'''
                if locationkey:
                    query = query[:-1] + '''  AND partof = %s;'''
                    cursor.execute(query, (location_name, locationkey))
                else:
                    query = query[:-1] + '''  AND partof IS NULL;'''
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
                        sub = self.get_location(sublocation[0])
                        self.delete_location(sub)
                query = '''DELETE FROM preferred_locations WHERE locationkey = %s;'''
                cursor.execute(query, [location.key])
                self.connection.commit()

        except Exception as e:
            print(f"Error deleting location from the database: {e}")

    def get_location(self, locationkey):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(description, '/', -1),'-',-1), locationtype, ispublicvenue, partof FROM preferred_locations as p
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
                cursor.execute(query, (location_id, location.path["building"].name, location.key, location.isPublic, location.name))
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

    def get_path(self, locationkey):
        try:
            path = {"building": "", "floor": "", "room": ""}
            location = self.get_location(locationkey)
            path[location.type] = location.name 
            while location.partof:
                location = self.get_location(location.partof)
                path[location.type] = location
            return path
        except Exception as e:
            print(f"Error getting path: {e} {locationkey}")

    def get_map_image(self, location_key):
        try:
            with self.connection.cursor() as cursor:
                query = '''SELECT l.mapimageurl FROM preferred_locations as p
                            JOIN locations AS l
                                ON l.room IN(
                            SELECT locationkey FROM preferred_locations
                            WHERE partof = %s) LIMIT 1;'''
                cursor.execute(query, [location_key])
                url = cursor.fetchall()
                return url[0]
        except Exception as e:
            print(f"Error getting map_image: {e} {location_key}")