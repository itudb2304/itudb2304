class Location:
    def __init__(self, name, objects) -> None:
        self.name = name
        self.objects = objects

class LocationsRepository:
    def __init__(self, connection) -> None:
        self.connection = connection
        
    def get_buildings(self):
        buildings = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT DISTINCT p.description, p.locationkey FROM preferred_locations AS p
                JOIN locations AS l
                ON l.site = p.description 
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
    
    def get_room(self, room_id):
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
        room = Location(room_name, objects)
        return room
    
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