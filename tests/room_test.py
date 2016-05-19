import unittest
from ..main.app import Amity
import sqlite3

import os


class roomstest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
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



    def test_allocate_housing(self):
        self.assertEqual(self.amity.allocate_housing('Margie Rain', 'lilac'), ('Margie Rain', 'lilac'))

    def test_allocate_housing(self):
        self.assertEqual(self.amity.allocate_housing('Margie Rain', 'Ruby'), ('Ruby', 'Margie Rain'))


    def test_save_file_path(self):
        self.assertEqual(self.amity.save_file_path('allocation.txt'), 'allocation.txt')

    def test_print_room(self):
        self.assertEqual(self.amity.print_room('php'), (type("")))


    def tearDown(self):
        self.amity = None



if __name__ == '__main__':
    unittest.main()
