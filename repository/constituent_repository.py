class ConstituentRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_all_constituents(self):
        constituents = []
        with self.connection.cursor() as cursor:
            query = "SELECT preferreddisplayname, forwarddisplayname FROM constituents LIMIT 500;"
            cursor.execute(query)
            constituents = cursor.fetchall()
        return constituents

    # def get_constituent_by_id(self, id):
    #     with self.db as connection:
    #         with connection.cursor() as cursor:
    #             query = f"SELECT * FROM constituents WHERE constituentid={id};"
    #             cursor.execute(query)
    #             # NOT COMPLETED
