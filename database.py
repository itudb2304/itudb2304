from location import Location
import mysql.connector

class Database:
    def __init__(self, host='localhost', user='root', password='', database='national_art'):
        self.db = mysql.connector.connect(host=host, user=user, password= password, database=database)
        self.locations = {}

    def get_all_buildings(self):
        buildings = []
        self.db.reconnect()
        with self.db as connection:
            cursor = connection.cursor()
            query = "SELECT DISTINCT site, locationid FROM locations;"
            cursor.execute(query)
            for building, locationid in cursor:
                buildings.append((locationid, building))
        return buildings
    
    def get_building(self, location_key):
        self.db.reconnect()
        with self.db as connection:
            cursor = connection.cursor()
            query = "SELECT site, description FROM locations WHERE (ID = ?);"
            cursor.execute(query, (location_key))
            building, description = cursor.fetchone()
        building_ = Location(building=building, location_key=location_key, description=description )
        return building