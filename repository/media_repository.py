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
        query = f"SELECT thumbnailurl, title, description, playurl FROM constituents_media;"

        cursor.execute(query)
        media = cursor.fetchall()

        return media
    
    def get_constituent_media_by_id(self, id):
        cursor = self.connection.cursor()
        
        query = f"SELECT thumbnailurl FROM constituents_media WHERE relatedid = {id}"

        cursor.execute(query)
        media = cursor.fetchall()

        return media
    
    def get_object_media(self, obj):
        cursor = self.connection.cursor()

        # Use parameterized queries to avoid SQL injection
        query = '''
            SELECT thumbnailurl
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

    def add_media(self, media):
        id = self.create_media(media)
        cursor = self.connection.cursor()
        query = '''INSERT INTO constituents_media (mediaid, title, description, thumbnailurl, playurl) VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (media.mediaid, media.title, media.description, media.thumbnailurl, media.playurl))
        self.connection.commit()
        return id
    
    def update_media(self, media):
        print(media.mediaid)
        cursor = self.connection.cursor()
        query = '''UPDATE constituents_media SET title = %s, description = %s, thumbnailurl = %s, playurl = %s WHERE mediaid = %s'''
        cursor.execute(query, (media.mediaid, media.title, media.description, media.thumbnailurl, media.playurl))
        self.connection.commit()

    def delete_media(self, media):
        cursor = self.connection.cursor()
        query = '''DELETE FROM constituents_media WHERE mediaid = %s'''
        cursor.execute(query, [media.mediaid])
        self.connection.commit() 

