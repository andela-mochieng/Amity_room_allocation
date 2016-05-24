import unittest
from ..main.app import Amity, welcome_msg
import sqlite3
import os
import ipdb

class roomstest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity("test.sqlite")

    def test_create_rooms(self):
        self.amity.create_rooms(
            ["lilac", "Camelot", "Vallhalla", "Oculus"], "O")
        self.amity.create_rooms(["Php", "Ruby", "Emerald", "Cedar"], "L")

        self.assertEqual(len(self.amity.rooms['O']), 4)
        self.assertEqual(len(self.amity.rooms['L']), 4)
        self.assertEqual(self.amity.rooms['O'][0], 'lilac')
        self.assertEqual(self.amity.rooms['L'][2], 'Emerald')

    def test_add_person(self):

        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        self.assertNotEqual(len(self.amity.people_data['Fellow']), 0)
        self.assertEqual(
            self.amity.people_data['Fellow'][0].get('Margie Rain'), 'Y')
        self.amity.add_person("Chidi", "Nnadi", "Staff", 'N')
        self.assertNotEqual(len(self.amity.people_data['Staff']), 0)

        self.assertEqual(
            self.amity.people_data['Staff'][0], 'Chidi Nnadi')


    def test_get_rooms(self):
        self.test_create_rooms()
        offices = self.amity.get_rooms('O')
        self.assertEqual(len(offices), 4)
        self.assertEqual(str(offices[0]['name']), 'lilac')
        living = self.amity.get_rooms('L')
        self.assertEqual(len(living), 4)
        self.assertEqual(str(living[2]['name']), 'Emerald')

    def test_allocation_rule(self):
        self.test_create_rooms()
        self.test_add_person()
        self.amity.allocation_rule("Margie Rain", "Fellow", "Y")
        office_allocations = self.amity.get_allocations("office_accommodation not null and name = 'Margie Rain'" )
        self.assertNotEqual(office_allocations, None)

        housing_allocations = self.amity.get_allocations("living_accomodation not null and name = 'Margie Rain'" )
        self.assertNotEqual(housing_allocations, None)



    def test_reallocate_person(self):
        '''Testing reallocation of persons'''
        self.test_allocation_rule()
        self.amity.reallocate_person(1, "Camelot")
        reallocate = self.amity.get_allocations("Persons.id = 1")
        self.assertEqual(str(reallocate[0]['office_accommodation']), "Camelot")
        self.amity.reallocate_person(1, "Cedar")
        reallocate = self.amity.get_allocations("Persons.id = 1")
        self.assertEqual(str(reallocate[0]['living_accomodation']), "Cedar")




    def tearDown(self):
        self.amity.drop_db()
        self.amity = None




if __name__ == '__main__':
    unittest.main()
