class Artwork:
    def __init__(self, uuid, iiifthumburl ,modified,maxpixels,height, iiifurl = None, viewtype = None,sequence = None,width = None,created = None,depictstmsobjectid = None,assistivetext = None) -> None:
        self.uuid = uuid
        self.iiifurl = None
        self.iiifthumburl = iiifthumburl
        self.viewtype = None
        self.sequence = None
        self.width = None
        self.height = height
        self.maxpixels = maxpixels
        self.created = None
        self.modified = modified
        self.depictstmsobjectid = None
        self.assistivetext = None

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
        query = '''INSERT INTO published_images (uuid, iiifthumburl, modified, maxpixels, height) VALUES(%s, %s, %s, %s, %s)'''
        cursor.execute(query, (artwork.uuid, artwork.iiifthumburl, artwork.modified, artwork.maxpixels, artwork.height))
        self.connection.commit()
        return id
    
    def update_artwork(self, artwork):
        print(artwork.uuid)
        cursor = self.connection.cursor()
        query = '''UPDATE published_images SET iiifthumburl = %s, modified = %s, maxpixels = %s, height = %s WHERE uuid = %s'''
        cursor.execute(query, (artwork.iiifthumburl, artwork.modified, artwork.maxpixels, artwork.height, artwork.uuid))
        self.connection.commit()

    def delete_artwork(self, artwork):
        cursor = self.connection.cursor()
        query = '''DELETE FROM published_images WHERE uuid = %s'''
        cursor.execute(query, [artwork.uuid])
        self.connection.commit() 
