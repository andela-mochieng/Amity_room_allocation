import sqlite3


class DataManager(object):
    """a connention to the db is initiated inorder to create
    insert, retrieve and delete data """

    def __init__(self, db):
        """ we connect to the db if tables are not """
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
        if self.table_num() < 1:
            self.create_tables()

    def query_db(self, data):
        self.c.execute(data)
        self.conn.commit()
        return self.c

    def table_num(self):
        """Gets a the number of tables present in the database"""

        cursor = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name")
        return len(cursor.fetchall())

    def close_db(self):
        """ closing connenction to the db"""
        self.conn.close()

    def create_tables(self):
        """ creating tables if they don't exist """
        self.query_db = ("CREATE TABLE IF NOT EXITS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    Office_name TEXT,Living_name TEXT)")

        self.query_db = ("CREATE TABLE IF NOT EXITS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    Name TEXT NOT NULL, staff_type Text NOT NULL, Boarding INT)")

        self.query_db = ("CREATE TABLE IF NOT EXIT Allocations(id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    Personnel_Name TEXT NOT NULL,Personnel_type TEXT NOT NULL,\
                    Room_name TEXT NOT NULL,Room_type TEXT NOT NULL)")
