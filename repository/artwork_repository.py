class Artwork:
    def __init__(self, uuid, iiifthumburl, created, depictstmsobjectid, assistivetext, iiifurl=None, modified=None, maxpixels=None, height=None, viewtype=None, sequence=None, width=None):
        self.uuid = uuid
        self.iiifthumburl = iiifthumburl
        self.created = created
        self.depictstmsobjectid = depictstmsobjectid
        self.assistivetext = assistivetext
        self.iiifurl = iiifurl  # Provide a default value (None or a default URL, for example)
        self.modified = modified
        self.maxpixels = maxpixels
        self.height = height
        self.viewtype = viewtype
        self.sequence = sequence
        self.width = width


class ArtworkRepository:
    def __init__(self, connection):
        self.connection = connection
    def get_all_artwork(self):
        cursor = self.connection.cursor()
        query = "SELECT iiifthumburl, modified, maxpixels, height, uuid FROM published_images LIMIT 500;"
        cursor.execute(query)
        artwork = cursor.fetchall() 
        return artwork
    
    def get_artwork(self, uuid):
        cursor = self.connection.cursor()
        query = "SELECT iiifthumburl, modified, maxpixels, height FROM published_images WHERE uuid = %s LIMIT 500;"
        cursor.execute(query, [uuid])
        artwork = cursor.fetchall() 
        return artwork
    
    def create_artwork(self, artwork):
        artwork.uuid = artwork.uuid
        return id

    def add_artwork(self, artwork):
        id = self.create_artwork(artwork)
        cursor = self.connection.cursor()
        query = '''INSERT INTO published_images (uuid, iiifthumburl, assistivetext, created, depictstmsobjectid) VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (artwork.uuid, artwork.iiifthumburl,artwork.assistivetext,artwork.created,artwork.depictstmsobjectid))
        self.connection.commit()
        return id
    
    def update_artwork(self, artwork):
        print(artwork.uuid)
        cursor = self.connection.cursor()
        query = '''UPDATE published_images SET iiifthumburl = %s, assistivetext = %s, created = %s WHERE uuid = %s'''
        cursor.execute(query, (artwork.iiifthumburl, artwork.assistivetext, artwork.created, artwork.uuid))
        self.connection.commit()

    def delete_artwork(self, artwork):
        cursor = self.connection.cursor()
        query = '''DELETE FROM published_images WHERE uuid = %s'''
        cursor.execute(query, [artwork.uuid])
        self.connection.commit() 

    def validation_objectid(self, objectid):
        cursor = self.connection.cursor()
        query = '''SELECT COUNT(objectid) FROM objects WHERE objectid = %s'''
        cursor.execute(query, (objectid,))
        result = cursor.fetchall()
        return result
    
    def validation_artworkid(self, artworkid):
        cursor = self.connection.cursor()
        query = '''SELECT COUNT(uuid) FROM published_images WHERE uuid = %s'''
        cursor.execute(query, (artworkid,))
        result = cursor.fetchall()
        return result
    
    def get_object_ids(self):
        object_ids = []
        cursor = self.connection.cursor()
        query = '''SELECT objectid FROM objects LIMIT 10;'''
        cursor.execute(query)
        object_ids = cursor.fetchall()
        self.connection.commit()
        return object_ids
    
    
        
