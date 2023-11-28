class AdminRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_table_names(self):
        table_names = []
        with self.connection.cursor() as cursor:
            query = "SHOW TABLES;"
            cursor.execute(query)
            # return list of table names
            table_names = [table[0] for table in cursor.fetchall()]
        return table_names
    
    def get_table_content(self, table_name):
        table_headers = []
        table_content = []
        with self.connection.cursor() as cursor:
            query = f"SHOW COLUMNS FROM {table_name};"
            cursor.execute(query)
            table_headers = [column[0] for column in cursor.fetchall()]
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                table_content.extend(rows)
        return table_headers, table_content
    
    '''def get_table_content(self, table_name):
        table_headers = []
        table_content = []
        self.db.reconnect()
        with self.db as connection:
            cursor = connection.cursor()
            cursor.execute("SHOW COLUMNS FROM " + table_name + ";")
            table_headers = [column[0] for column in cursor.fetchall()]
            cursor.execute("SELECT * FROM " + table_name + ";")
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                table_content.extend(rows)
        return table_headers, table_content'''
