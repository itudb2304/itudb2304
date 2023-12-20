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
        queryobject = f"SELECT thumbnailurl, title, description, playurl FROM object_media;"

        cursor.execute(queryobject)
        mediaobject = cursor.fetchall()
        queryconstituent = f"SELECT thumbnailurl, title, description, playurl FROM constituents_media;"

        cursor.execute(queryconstituent)
        mediaconst = cursor.fetchall()
        media = mediaobject + mediaconst
        return media
    

    def get_constituent_media_search(self, id):
        cursor = self.connection.cursor()

        # Use LIMIT and OFFSET for pagination
        
        queryobject = "SELECT thumbnailurl, title, description, playurl FROM object_media WHERE mediaid = %s;"

        cursor.execute(queryobject, (id,))
        mediaobject = cursor.fetchall()
        queryconstituent = "SELECT thumbnailurl, title, description, playurl FROM constituents_media WHERE mediaid = %s;"

        cursor.execute(queryconstituent, (id,))
        mediaconst = cursor.fetchall()
        media = mediaobject + mediaconst
        return media


    def get_constituent_media_by_id(self, id):
        if id is None:
            return []  #

        cursor = self.connection.cursor()

        query = '''
            SELECT thumbnailurl
            FROM constituents_media
            WHERE mediaid IN (
                SELECT mediaid
                FROM media_relationships
                WHERE relatedid = %s
                AND BINARY relatedentity = 'nga:art:tms:constituents\r');
        '''

        cursor.execute(query, (id,))
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

    def add_media(self, media, table):
        id = self.create_media(media)
        cursor = self.connection.cursor()
        if table == "Object":
            query = '''INSERT INTO constituents_media (mediaid, title, description, thumbnailurl, playurl) VALUES(%s, %s, %s, %s, %s)'''
        elif table == "Constituent":
            query = '''INSERT INTO object_media (mediaid, title, description, thumbnailurl, playurl) VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (media.mediaid, media.title, media.description, media.thumbnailurl, media.playurl))
        self.connection.commit()
        return id

    def update_media(self, media, table):
        print(media.mediaid)
        cursor = self.connection.cursor()
        if table == "Object":
            query = '''UPDATE object_media SET title = %s, description = %s, thumbnailurl = %s, playurl = %s WHERE mediaid = %s'''
        elif table == "Constituent":
            query = '''UPDATE constituents_media SET title = %s, description = %s, thumbnailurl = %s, playurl = %s WHERE mediaid = %s'''
        cursor.execute(query, (media.mediaid, media.title, media.description, media.thumbnailurl, media.playurl))
        self.connection.commit()
    

    def delete_media(self, media, table):
        cursor = self.connection.cursor()
        
        if table == "Object":
            query = '''DELETE FROM object_media WHERE mediaid = %s'''
            
        elif table == "Constituent":
            query = '''DELETE FROM constituents_media WHERE mediaid = %s'''
        cursor.execute(query, [media.mediaid])
        self.connection.commit()