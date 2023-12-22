class Media:
    def __init__(self, mediaid, title, description, thumbnailurl, playurl, mediatype = None,duration = None,language = None,downloadurl = None, keywords = None,tags = None, imageurl =None,presentationdate = None, releasedate = None, lastmodified = None) -> None:
        self.mediaid = mediaid
        self.title = title
        self.description = description
        self.thumbnailurl = thumbnailurl
        self.playurl = playurl


class MediaRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_constituent_media(self):
        cursor = self.connection.cursor()

        # Use LIMIT and OFFSET for pagination
        queryobject = """SELECT object_media.thumbnailurl, object_media.title, object_media.description, 
           object_media.playurl, media_relationships.relatedid
        FROM object_media
        JOIN media_relationships ON object_media.mediaid = media_relationships.mediaid;"""
        cursor.execute(queryobject)
        mediaobj = cursor.fetchall()
  
        return mediaobj
    

    def get_constituent_media_search(self, title):
        cursor = self.connection.cursor()
        queryobject = """SELECT object_media.thumbnailurl, object_media.title, object_media.description, 
           object_media.playurl, media_relationships.relatedid
        FROM object_media
        JOIN media_relationships ON object_media.mediaid = media_relationships.mediaid WHERE title LIKE %s;"""
        cursor.execute(queryobject, (f'{title}%',))
        mediaobj = cursor.fetchall()
        return mediaobj


    def get_object_media(self, obj):
        cursor = self.connection.cursor()

        # Use parameterized queries to avoid SQL injection
        query = '''
            SELECT playurl, title
                FROM object_media
                WHERE mediaid IN (
                    SELECT mediaid
                    FROM media_relationships
                    WHERE relatedid = %s
                    AND BINARY relatedentity = 'nga:art:tms:objects\r');'''
        cursor.execute(query, (obj.objectid,))
        media = cursor.fetchall()

        return media

    def create_media(self, media):
        media.mediaid = media.mediaid
        return id

    def add_media(self, media, related):
        id = self.create_media(media)
        cursor = self.connection.cursor()
        media_relationships_query = '''INSERT INTO media_relationships (mediaid, relatedid, relatedentity) VALUES (%s, %s, %s)'''
        relatedentity = "nga:art:tms:objects"
        cursor.execute(media_relationships_query, (media.mediaid,related, relatedentity))
        self.connection.commit()
        query = '''INSERT INTO object_media (mediaid, title, description, thumbnailurl, playurl) VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (media.mediaid, media.title, media.description, media.thumbnailurl, media.playurl))
        self.connection.commit()
        return id

    def update_media(self, media):
        print(media.mediaid)
        cursor = self.connection.cursor()
        query = '''UPDATE object_media SET title = %s, description = %s, thumbnailurl = %s, playurl = %s WHERE mediaid = %s'''
       
        cursor.execute(query, (media.title, media.description, media.thumbnailurl, media.playurl,media.mediaid))
        self.connection.commit()
    

    def delete_media(self, media):
        cursor = self.connection.cursor()
        query = '''DELETE FROM object_media WHERE mediaid = %s'''
            
        cursor.execute(query, [media.mediaid])
        self.connection.commit()
