import sqlite3


class DataBase:
    def __init__(self, table, fields, db_path='students.db'):
        self.conn = sqlite3.connect(db_path)
        self.table = table
        self.fields = fields
        self.create_table()


    def create_table(self):
        with self.conn:
            query = f"CREATE TABLE IF NOT EXISTS {self.table} ({self.fields})"
            self.conn.execute(query)
    
    
    def is_empty(self):
        query = f"SELECT COUNT(*) FROM {self.table}"
        result = self.conn.execute(query).fetchone()
        return result[0] == 0


    def insert_data(self, data):
        with self.conn:
            fields = ', '.join([f':{field}' for field in data.keys()])
            query = f'INSERT INTO {self.table} VALUES ({fields})'
            self.conn.execute(query, data)


    def get_all_data(self):
        with self.conn:
            query = f'SELECT * FROM {self.table}'
            cursor = self.conn.execute(query)
            # rows = cursor.fetchall()
            return cursor.fetchall()


    def get_by_criteria(self, by): #one item dict
        field = list(by.keys())[0]
        with self.conn:
            by_field = ' AND '.join([f'{field} = :{field}' for field in by.keys()])
            query = f'SELECT * FROM {self.table} WHERE {by_field}'
            cursor = self.conn.execute(query, by)
            return cursor.fetchall()
      
        

    def get_field_by_criterias(self, field):
        with self.conn:
            query = f'SELECT {field} FROM {self.table}'
            cursor = self.conn.execute(query)
            return cursor.fetchall()


    def update_by_criteria(self, set_object): 
        by_field = list(set_object.keys())[0]
        fields = ', '.join([f'{field} = :{field}' for field in set_object.keys()])
        with self.conn:
            query = f'UPDATE {self.table} SET {fields} WHERE {by_field} = :{by_field}'
            self.conn.execute(query, set_object)

   
    def delete_row(self, by):
        fields = ' AND '.join([f'{field} = :{field}' for field in by.keys()])
        with self.conn:
            query = f'DELETE FROM {self.table} WHERE {fields}'
            self.conn.execute(query, by)
     
