from models.object import ObjectDTO
from models.object_text_entry import objectTextEntryDTO

class LocationDTO:
    def __init__(self, data):
        self.locationid, self.site, self.room, self.publicaccess, self.description, self.unitposition, \
        self.mapimageurl = self._handle_none_values(data)

    def _handle_none_values(self, data):
        return tuple(None if value is None else value for value in data)

class ObjectsRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def get_all_objects(self, selected_classifications=None, title_filter=None, credit_line_filter=None, sort_by_title="None", limit=0, offset=0):
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
                if sort_by_title != "none":
                    if sort_by_title == "asc":
                        query = query[:-1] + " ORDER BY title ASC;"
                    else:
                        query = query[:-1] + " ORDER BY title DESC;"
                if limit:
                    query = query[:-1] + " LIMIT %s;"
                    execution_list.append(limit)
                if offset:
                    query = query[:-1] + " OFFSET %s;"
                    execution_list.append(offset)
                
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
                cursor.execute(query, [objectid])
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
    
    def get_object_constituents(self, objectid):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                SELECT 
                    oc.constituentid,
                    c.preferreddisplayname,
                    c.forwarddisplayname
                FROM 
                    objects_constituents oc
                JOIN 
                    objects o ON oc.objectid = o.objectid
                JOIN 
                    constituents c ON oc.constituentid = c.constituentid
                WHERE 
                    oc.objectid = %s 
                    AND oc.roletype = "artist";
                '''
                cursor.execute(query, [objectid])
                rows = cursor.fetchall()
                constituents = []
                for row in rows:
                    constituents.append([row[0],row[1],row[2]])
            return constituents
        except Exception as e:
            print(f"Error getting object constituents from the database: {e}")
    
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

    def get_media_by_objectid(self, objectid):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                SELECT iiifthumburl, assistiveText
                FROM published_images
                WHERE depictstmsobjectid=%s;
                '''
                cursor.execute(query, [objectid])
                rows = cursor.fetchall()
                media = []
                for row in rows:
                    media.append([row[0],row[1]])
            return media
        except Exception as e:
            print(f"Error getting media from the database: {e}")
            self.connection.rollback()
    
    def add_media_to_object(self, objectid, url, assistiveText):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                INSERT INTO published_images (uuid, iiifurl, iiifthumburl, depictstmsobjectid, assistiveText)
                VALUES (%s, %s, %s, %s, %s);
                '''
                cursor.execute(query, [url, url, url, objectid, assistiveText])
                self.connection.commit()
        except Exception as e:
            print(f"Error adding media to the database: {e}")
            self.connection.rollback()
    
    def edit_media_of_object(self, objectid, assistiveText):
        try:
            with self.connection.cursor() as cursor:
                query = '''
                UPDATE published_images
                SET assistiveText = %s
                WHERE depictstmsobjectid = %s;
                '''
                cursor.execute(query, [assistiveText, objectid])
                self.connection.commit()
        except Exception as e:
            print(f"Error editing media in the database: {e}")
            self.connection.rollback()
