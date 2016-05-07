import unittest
import sqlite3
from ..db.d_base import Dbase_centre


class Dbase_centreTests(unittest.TestCase):
    """ testing the db functionalities"""

    def test_query_db(self):
        # test if a cursor object is returned
        # after db connection

        db = Dbase_centre('amity.sqlite')
        query = "INSERT INTO Rooms VALUES(?, ?, ?, ? )"
        record = [(("x"), ("dummy name"), ("fellow"), ("y"))]
        db = Dbase_centre('amity.sqlite')
        cur = db.query_db(query, record)
        self.assertEqual(type(cur), sqlite3.Cursor)

    # def test_create_tables(self):
    #     """test whether function creates 2 tables"""
    #     pass


if __name__ == '__main__':
    unittest.main()
