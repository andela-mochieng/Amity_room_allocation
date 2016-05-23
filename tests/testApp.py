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
        name = self.name = ""
        personnel_type = self.personnel_type = ""
        want_accommodation = self.want_accommodation = ""

    def test_add_person(self):
        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        name = "Margie Rain"
        person_type = "Fellow"
        want_accommodation = "Y"
        self.assertEqual(self.amity.add_person(
            'Margie', 'Rain', 'Fellow', 'Y'), 'Margie Rain Fellow Y')

    def test_print_allocations(self):
        if self.amity.print_allocations():
            self.assertEqual(self.amity.print_allocations(), type(""))


    def test_print_unallocated(self):
        if self.amity.print_unallocated():
            self.assertEqual(self.amity.print_unallocated(), type(""))

    def test_print_room(self):
        room =self.amity.print_room('Ruby')
        self.assertEqual(room, type(""))

    def test_save_file_path(self):
        self.assertEqual(self.amity.save_file_path(
            'allocation.txt'), 'allocation.txt')

    def test_write_to_file(self):
        write_file = self.amity.write_to_file("allocations.txt", "allocations")
        with open("allocations.txt", 'a+') as f:
            lines = f.readlines()
        self.assertTrue(write_file, "allocations.txt")

    def tearDown(self):
        self.amity = None


if __name__ == '__main__':
    unittest.main()
