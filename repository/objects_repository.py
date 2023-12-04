class ObjectDTO:  # Data Transfer Object
    def __init__(self, data):
        self.objectid, self.accessioned, self.accessionnum, self.locationid, self.title, self.displayDate, self.beginYear, \
        self.endYear, self.visualBrowserTimeSpan, self.medium, self.dimensions, self.inscription, self.markings, \
        self.attributionInverted, self.attribution, self.provenanceText, self.creditLine, self.classification, \
        self.subClassification, self.visualBrowserClassification, self.parentid, self.isVirtual, self.departmentabbr, \
        self.portfolio, self.series, self.volume, self.watermarks, self.lastDetectedModification, self.wikidataid, \
        self.customPrintURL = self._handle_none_values(data)

    def _handle_none_values(self, data):
        return tuple(None if value is None else value for value in data)

class LocationDTO:
    def __init__(self, data):
        self.locationid, self.site, self.room, self.publicaccess, self.description, self.unitposition, \
        self.mapimageurl = self._handle_none_values(data)

    def _handle_none_values(self, data):
        return tuple(None if value is None else value for value in data)

class ObjectsRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def get_all_objects(self):
        with self.connection.cursor() as cursor:
            query = '''
            SELECT objectid, accessioned, accessionnum, locationid, title, displayDate, beginYear, 
                endYear, visualBrowserTimeSpan, medium, dimensions, inscription, markings, attributionInverted, 
                attribution, provenanceText, creditLine, classification, subClassification, visualBrowserClassification, 
                parentid, isVirtual, departmentabbr, portfolio, series, volume, watermarks, lastDetectedModification, 
                wikidataid, customPrintURL 
            FROM objects;'''
            cursor.execute(query)
            objects = [ObjectDTO(row) for row in cursor.fetchall()]
        return objects
    
    def get_object_by_objectid(self, objectid):
        with self.connection.cursor() as cursor:
            query = '''
            SELECT objectid, accessioned, accessionnum, locationid, title, displayDate, beginYear, 
                endYear, visualBrowserTimeSpan, medium, dimensions, inscription, markings, attributionInverted, 
                attribution, provenanceText, creditLine, classification, subClassification, visualBrowserClassification, 
                parentid, isVirtual, departmentabbr, portfolio, series, volume, watermarks, lastDetectedModification, 
                wikidataid, customPrintURL
            FROM objects
            WHERE objectid = %s;
            '''
            cursor.execute(query, [objectid]) #objectid is a number but it is passed as a string
            row = cursor.fetchone()
            object = ObjectDTO(row)
        return object

    def get_location_by_locationid(self, locationid):
        with self.connection.cursor() as cursor:
            query = '''
            SELECT locationid, site, room, publicaccess, description, unitposition, mapimageurl
            FROM locations
            WHERE locationid = %s;
            '''
            cursor.execute(query, [locationid])
            row = cursor.fetchone()
            location = LocationDTO(row)
        return location
