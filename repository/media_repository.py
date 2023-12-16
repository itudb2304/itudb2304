class MediaRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_media(self, page, per_page=100):
        offset = (page - 1) * per_page
        cursor = self.connection.cursor()

        # Use LIMIT and OFFSET for pagination
        query = f"SELECT thumbnailurl, title, description, playurl FROM constituents_media LIMIT %s OFFSET %s;"

        cursor.execute(query, (per_page, offset))
        media = cursor.fetchall()

        return media
