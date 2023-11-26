from location import Location
import mysql.connector

class Database:
    def __init__(self, host='localhost', user='root', password='', database='national_art'):
        self.db = mysql.connector.connect(host=host, user=user, password= password, database=database)
        self.locations = {}

    def get_table_names(self):
        tables = []
        self.db.reconnect()
        with self.db as connection:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in cursor.fetchall()]
        return tables
    
    def get_table_content(self, table_name):
        table_headers = []
        table_content = []
        self.db.reconnect()
        with self.db as connection:
            cursor = connection.cursor()
            cursor.execute("SHOW COLUMNS FROM " + table_name + ";")
            table_headers = [column[0] for column in cursor.fetchall()]
            cursor.execute("SELECT * FROM " + table_name + ";")
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                table_content.extend(rows)
        return table_headers, table_content


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
    
    def get_all_constituents(self):
        constituents = []
        self.db.reconnect()
        with self.db as connection:
            with connection.cursor() as cursor:
                query = "SELECT preferreddisplayname, forwarddisplayname FROM constituents LIMIT 500;"
                cursor.execute(query)
                constituents = cursor.fetchall()
        return constituents
    