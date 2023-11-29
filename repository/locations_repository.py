class Location:
    def __init__(self, building) -> None:
        self.building = building
        self.floors = []

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
                WHERE p.locationtype = "building"; 
            '''
            cursor.execute(query)
            for building, id in cursor:
                buildings.append((building, id))
        return buildings
    
    def get_floors(self, building_id):
        floors = []
        with self.connection.cursor() as cursor:
            query = '''
                SELECT p.description, p.locationkey FROM preferred_locations as p
                WHERE p.partof = %s;
            '''
            cursor.execute(query, [building_id])
            for description, floors_id in cursor:
                floors.append((description, floors_id))
        return floors