import unittest
from ..main.app import Amity
import sqlite3

import os


class roomstest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.conn = sqlite3.connect("test_amity.sqlite")
        self.connect = self.conn.cursor()
        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, type TEXT)")
        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Personnel_type TEXT, want_accommodation TEXT, office_accommodation TEXT , living_accomodation TEXT)")
        self.rooms = {
            'O': [],
            'L': []
        }

        self.people_data = {'Staff': [],
                            'Fellow': []
                            }


    def test_add_person(self):
        self.assertEqual(self.amity.add_person('Margie', 'Rain', 'Fellow', 'Y'), 'Margie Rain Fellow Y')


    def test_office_space_count(self):
        self.assertEqual(self.amity.office_space_count('Camelot'), 0)

    def test_living_space_count(self):
        self.assertEqual(self.amity.living_space_count('Ruby'), 0)


    # def test_allocation_rule(self):
    #     self.assertEqual(self.amity.allocation_rule('Margie Rain', 'Fellow', 'Y'))

    # def test_insert_db(self):
    #     pass

    def test_allocate_housing(self):
        self.assertEqual(self.amity.allocate_housing('Margie Rain', 'lilac'), ('Margie Rain', 'lilac'))

    def test_allocate_housing(self):
        self.assertEqual(self.amity.allocate_housing('Margie Rain', 'Ruby'), ('Ruby', 'Margie Rain'))

    def test_reallocate_person(self):
        self.assertEqual(self.amity.reallocate_person('1', 'php'),('Margie Rain', 'php'))






    def tearDown(self):
        self.amity = None
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
