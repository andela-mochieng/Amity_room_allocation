import unittest
from ..main.app import Amity, welcome_msg
import sqlite3
import os
import ipdb


class roomstest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity("test.sqlite")

    def test_create_rooms(self):
        '''Test whether rooms are created and saved'''
        self.amity.create_rooms(
            ["lilac", "Camelot", "Vallhalla", "Oculus"], "O")
        self.amity.create_rooms(["Php", "Ruby", "Emerald", "Cedar"], "L")
        self.assertEqual(self.amity.rooms.keys(), ['L', 'O'])
        self.assertEqual(len(self.amity.rooms['L'].keys()), 4  )
        self.assertEqual(len(self.amity.rooms['O'].keys()), 4)


    def test_add_person(self):
        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        self.amity.add_person("Chidi", "Nnadi", "Staff", 'N')
        self.amity.add_person("Margie", "Akoth", "Fellow", "N")
        self.assertEqual(len(self.amity.people['fellow to house']), 1)
        self.assertEqual(len(self.amity.people['staff and fellow']), 2)
        self.assertEqual(self.amity.rooms, {'L': {}, 'O': {}})


    def test_allocate_room(self):
        room_type = 'O' or 'L'
        self.assertEqual(len(self.amity.unallocated[room_type]), 0)
        self.assertEqual(self.amity.rooms, {'L': {}, 'O': {}})
        # ipdb.set_trace()
        self.assertTrue(self.amity.space.is_filled(3), False)
        self.assertTrue(self.amity.space.is_filled(7), True)



















    def tearDown(self):
        self.amity = None


if __name__ == '__main__':
    unittest.main()
