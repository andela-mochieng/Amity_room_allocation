import unittest
import sqlite3
import os
from ..main.amity import Amity, welcome_msg
from ..main.models.person import Person, Fellow, Staff
from ..main.models.room import Office, LivingSpace
import ipdb


class amitytest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity("test.sqlite")
        self.amity.rooms = []
        self.amity.people = []

        self.amity.create_rooms({
            '<room_name>': ['Room 1', 'Room 2', 'Room 3', 'Room4'],
            '<room_type>': ['living', 'living', 'office', 'office'],
        })
        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        self.amity.add_person("Chidi", "Nnadi", "Staff", 'N')
        self.amity.add_person("Margie", "Akoth", "Fellow", "N")

    def test_create_room(self):
        """Test creation of rooms"""
        self.assertEqual(4, len(self.amity.rooms))
        self.assertEqual(self.amity.rooms[-1].name, 'Room4')

    def test_add_person(self):
        """ Test that people are added to the system"""
        self.assertEqual(len(self.amity.people), 3)
        self.assertEqual(self.amity.people[1].name, 'Chidi Nnadi')





    def tearDown(self):
        self.amity=None


if __name__ == '__main__':
    unittest.main()
