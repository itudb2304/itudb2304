class ObjectDTO:  # Data Transfer Object
    def __init__(self, data=None):
        if data is None:
            self.objectid = None
            self.accessioned = None
            self.accessionnum = None
            self.locationid = None
            self.title = None
            self.displayDate = None
            self.beginYear = None
            self.endYear = None
            self.visualBrowserTimeSpan = None
            self.medium = None
            self.dimensions = None
            self.inscription = None
            self.markings = None
            self.attributionInverted = None
            self.attribution = None
            self.provenanceText = None
            self.creditLine = None
            self.classification = None
            self.subClassification = None
            self.visualBrowserClassification = None
            self.parentid = None
            self.isVirtual = None
            self.departmentabbr = None
            self.portfolio = None
            self.series = None
            self.volume = None
            self.watermarks = None
            self.lastDetectedModification = None
            self.wikidataid = None
            self.customPrintURL = None
        else:
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

class objectTextEntryDTO:
    texttypes = [ "bibliography", "exhibition_history", "lifetime_exhibition", "other_collections", "exhibition_history_footnote", "documentary_labels_inscriptions", "inscription_footnote"]

    def __init__(self, data):
        text_entries = {text_type: [] for text_type in self.texttypes}

        for row in data:
            text_type = row[2]
            if text_type in self.texttypes:
                text_entries[text_type].append([row[1], row[3]]) #text, year
        self.text_entries = text_entries

classification_elements = ["Painting", "Print", "Sculpture", "Drawing","Volume", "Portfolio","Photograph","New Media","Decorative Art","Technical Material"]

class ObjectsRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def get_all_objects(self, selected_classifications=None, title_filter=None, credit_line_filter=None):
        try:
            with self.connection.cursor() as cursor:
                execution_list = []
                if selected_classifications:
                    for classification in selected_classifications:
                        execution_list.append(classification)
                if title_filter:
                    execution_list.append('%' + title_filter + '%')
                if credit_line_filter:
                    execution_list.append('%' + credit_line_filter + '%')
                
                query = '''
                SELECT objectid, accessioned, accessionnum, locationid, title, displayDate, beginYear, 
                    endYear, visualBrowserTimeSpan, medium, dimensions, inscription, markings, attributionInverted, 
                    attribution, provenanceText, creditLine, classification, subClassification, visualBrowserClassification, 
                    parentid, isVirtual, departmentabbr, portfolio, series, volume, watermarks, lastDetectedModification, 
                    wikidataid, customPrintURL 
                FROM objects;'''
                if selected_classifications:
                    query = query[:-1] + " WHERE classification IN (" + ",".join(["%s"] * len(selected_classifications)) + ");"
                if title_filter:
                    if selected_classifications:
                        query = query[:-1] + " AND title LIKE %s;"
                    else:
                        query = query[:-1] + " WHERE title LIKE %s;"
                if credit_line_filter:
                    if selected_classifications or title_filter:
                        query = query[:-1] + " AND creditLine LIKE %s;"
                    else:
                        query = query[:-1] + " WHERE creditLine LIKE %s;"
                cursor.execute(query, execution_list)
                objects = [ObjectDTO(row) for row in cursor.fetchall()]
            return objects
        except Exception as e:
            print(f"Error getting all objects from the database: {e}")

    def get_object_text_entries(self, objectid):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                SELECT o.objectid, ot.text, ot.texttype, ot.year
                FROM objects o
                LEFT JOIN objects_text_entries ot ON o.objectid = ot.objectid
                WHERE o.objectid = %s;
                '''
                cursor.execute(query, [objectid])
                rows = cursor.fetchall()
                mappedentries = objectTextEntryDTO(rows)
            return mappedentries
        except Exception as e:
            print(f"Error getting object text entries from the database: {e}")


    def get_object_by_objectid(self, objectid):
        try:
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
        except Exception as e:
            print(f"Error getting object from its objectid from the database: {e}")

    def get_location_by_locationid(self, locationid):
        try:
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
        except Exception as e:
            print(f"Error getting location from its locationid from the database: {e}")
    
    def get_max_objectid(self):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                SELECT MAX(objectid) FROM objects;
                '''
                cursor.execute(query)
                max_objectid = cursor.fetchone()[0]
            return max_objectid
        except Exception as e:
            print(f"Error getting max objectid from the database: {e}")

    def add_object(self, objectDTO):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                INSERT INTO objects (objectid, accessioned, accessionnum, locationid, title, displayDate, beginYear, 
                    endYear, visualBrowserTimeSpan, medium, dimensions, inscription, markings, attributionInverted, 
                    attribution, provenanceText, creditLine, classification, subClassification, visualBrowserClassification, 
                    parentid, isVirtual, departmentabbr, portfolio, series, volume, watermarks, lastDetectedModification, 
                    wikidataid, customPrintURL)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s);
                '''
                cursor.execute(query, [objectDTO.objectid, objectDTO.accessioned, objectDTO.accessionnum, objectDTO.locationid, objectDTO.title, objectDTO.displayDate, objectDTO.beginYear, 
                    objectDTO.endYear, objectDTO.visualBrowserTimeSpan, objectDTO.medium, objectDTO.dimensions, objectDTO.inscription, objectDTO.markings, objectDTO.attributionInverted, 
                    objectDTO.attribution, objectDTO.provenanceText, objectDTO.creditLine, objectDTO.classification, objectDTO.subClassification, objectDTO.visualBrowserClassification, 
                    objectDTO.parentid, objectDTO.isVirtual, objectDTO.departmentabbr, objectDTO.portfolio, objectDTO.series, objectDTO.volume, objectDTO.watermarks, objectDTO.lastDetectedModification, 
                    objectDTO.wikidataid, objectDTO.customPrintURL])
                self.connection.commit()
        except Exception as e:
            print(f"Error adding object to the database: {e}")
            self.connection.rollback()
    
    def update_object(self, objectDTO):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                UPDATE objects
                SET accessioned = %s, accessionnum = %s, title = %s, displayDate = %s, beginYear = %s, endYear = %s, 
                    medium = %s, attribution = %s, creditLine = %s, classification = %s, isVirtual = %s
                WHERE objectid = %s;
                '''
                cursor.execute(query, [objectDTO.accessioned, objectDTO.accessionnum, objectDTO.title, objectDTO.displayDate, objectDTO.beginYear, objectDTO.endYear, 
                    objectDTO.medium, objectDTO.attribution, objectDTO.creditLine, objectDTO.classification, objectDTO.isVirtual, objectDTO.objectid])
              
                self.connection.commit()
        except Exception as e:
            print(f"Error updating object in the database: {e}")
            self.connection.rollback()
    
    def delete_object(self, objectid):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                DELETE FROM objects
                WHERE objectid = %s;
                '''
                cursor.execute(query, [objectid])
                self.connection.commit()
        except Exception as e:
            print(f"Error deleting object from the database: {e}")
            self.connection.rollback()