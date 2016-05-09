import sqlite3


class Dbase_centre(object):
    """initiates connention to amity.sqlite dasebase
    and returns a cursor when queried"""

    def __init__(self, db):
        """connects to db a returns cursor object"""
        self.conn = sqlite3.connect(db)
        self.connection = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        """creates tables if non_exists"""
        with self.conn:
            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS Rooms(Name TEXT, Room_type TEXT, capacity integer, available TEXT)")

            self.connection.execute(
                "CREATE TABLE IF NOT EXISTS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Personel_type TEXT, want_accommodation TEXT)")

    def query_db(self, query, record):
        """query the db and return connention"""
        self.connection.executemany(query, record)
        self.conn.commit()
        return self.connection

    def table_num(self):
        """ get num of table in db"""
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        record = [("Rooms", "Persons")]
        cursor = self.Dbase_centre.query_db(query, record)
        return len(cursor.fetchall())

    def insert_db(self, args):
        pass

    def select_db(self, query):
        with self.conn:
            self.connention.execute(query)
            return self.connection.fetchall()
