import unittest
from itertools import count
import sqlite3
import os
from ..main.amity import Amity
from ..main.models.person import Person, Fellow, Staff
from ..main.models.room import Office, LivingSpace


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

    def test_get_random_available_room(self):
        """ Test that personnel are allocated to rooms randomly"""
        room = self.amity.get_random_available_room('OFFICE')
        self.assertIn(room.name, ['Room 3', 'Room4'])
        self.assertEqual(self.amity.get_random_available_room('unknown'), None)
        room = self.amity.get_random_available_room('LIVING_SPACE')
        self.assertIn(room.name, ['Room 1', 'Room 2'])

    def test_amity_load_person(self):
        self.amity.people = []
        self.amity.load_people("tests/testData.txt")
        self.assertTrue(os.path.exists("tests/testData.txt"))
        self.assertTrue(len(self.amity.people), 3)

    def test_print_allocations(self):
        """
        Test that allocations are displayed on screen
        and printed to a text file if specified
        """
        self.amity.print_allocations({
            "--o": "testfile.txt"
        })
        # File is created
        self.assertTrue(os.path.exists("testfile.txt"))
        # Data is entered
        with open("testfile.txt") as testfile:
            lines = testfile.readlines()
            self.assertIn('Margie Rain,\n', lines)
        os.remove("testfile.txt")

    def test_print_room(self):
        self.assertEqual(self.amity.print_room(
            {'<name_of_room>': 'Room 1'}), None)

    def test_get_room_name(self):
        """ Test that we can search for a room by name"""
        self.amity.rooms = []
        self.amity.create_rooms({
            '<room_name>': ['Room 1'],
            '<room_type>': ['living'],
        })
        self.assertEqual(self.amity.get_room_name("Room 1").name, "Room 1")
        self.assertEqual(self.amity.get_room_name("Room1"), False)

    def test_reallocate_person(self):
        """Test that a person can be reallocated to a different room """
        self.amity.people = []
        Person.person_id = count(1)
        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        person = self.amity.people[0]
        if person.allocation['LIVING_SPACE'] == 'Room 1':
            new_room = "Room 2"
        else:
            new_room = "Room 1"
        self.amity.reallocate_person({
            '<person_id>': person._id,
            '<new_room_name>': new_room,
            '-l': True,
        })
        for person in self.amity.people:
            self.assertEqual(person.allocation[
                'LIVING_SPACE'], new_room)

    def test_get_person_id(self):
        """ Test that we can search personnel by id"""
        self.amity.people = []
        Person.person_id = count(1)
        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        self.assertEqual(self.amity.get_person_id("1").name,
                         'Margie Rain')
        self.assertEqual(self.amity.get_person_id(2), False)

    def test_save_state(self):
        """ Test whether data is save to the db """
        self.assertFalse(self.amity.create_tables(), False)
        self.amity.save_state('test.sqlite')
        conn = sqlite3.connect('test.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT * from People ")
        for row in cursor:
            # import ipdb; ipdb.set_trace()
            self.assertEqual(row[0], 1)
            self.assertEqual(row[1], 'Margie Rain')
            self.assertEqual(row[2], 'FELLOW')
            self.assertEqual(row[3], 'True')
            break

    def tearDown(self):

        self.amity = None


if __name__ == '__main__':
    unittest.main()
