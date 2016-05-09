import unittest
import sqlite3
from ..db.d_base import Dbase_centre


class Dbase_centreTests(unittest.TestCase):
    """ testing the db functionalities"""

    def _query_db(self):
        # test if a cursor object is returned
        # after db connection

        db = Dbase_centre('amity.sqlite')
        query = "INSERT INTO Persons VALUES(?, ?, ? )"
        record = [("dummy name"), ("fellow"), ("y")]
        cur = db.query_db(query, record)
        self.assertEqual(type(cur), sqlite3.Cursor)



if __name__ == '__main__':
    unittest.main()
