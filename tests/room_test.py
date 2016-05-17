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
        self.amity.add_person('Margie', 'Rain', 'Fellow', 'Y')
        self.name = 'Margie' + " " + 'Rain'
        self.person_type = 'Fellow'
        self.want_accommodation = 'Y'
        self.assertEqual(self.name, 'Margie Rain')
        self.assertEqual(self.person_type, 'Fellow')
        self.assertEqual(self.want_accommodation, 'Y')
        if self.person_type.upper() == 'STAFF':
            self.people_data['Staff'].append(name)
        else:
            self.people_data['Fellow'].append(
                {self.name: self.want_accommodation})
        self.assertTrue(
            self.people_data, {'Fellow': {'Margie Rain': 'Y'}, 'Staff': []})
        self.assertEqual(len(self.people_data['Staff']), 0)
        self.amity.allocation_rule(
            self.name, self.person_type, self.want_accommodation)

    def test_allocation_rule(self):
        self.amity.allocation_rule('Margie Rain', 'Fellow', 'Y')
        self.office_name = self.connect.execute(
            "SELECT Name FROM Rooms where type = 'L'").fetchall()
        for off_name in self.office_name:
            off_name = map(lambda x: x.encode('ascii'), off_name)
            self.assertTrue(type(off_name), "Ruby")

    # def test_load_people(self):
    #     amity.load_people(self, *args)
    #     files_path = amity.self.save_file_path(self, path)
    #     file_path = files_path.read_file()
    #     self.assertEqual(len(file_path), 1)
    #     parser = File.FileParser(
    #         os.path.dirname(os.path.realpath("load_data.txt")))
    #     list_allocations = parser.read_file()
    #     self.assertEqual(len(list_allocations), 7)

    # def test_living_space_count(self):
    #     self.assertEqual(type(self.amity.living_space_count.living_occupanted), 3)

    # # def test_allocate_office(self):
    # #     self.assertEqual(type(self.amity.reallocate_person.person_allocate, None))
    # #     self.assertEqual(self.amity.reallocate_person.new_room_name, self.amity.reallocate_person.self.living_allocate)



    # # def test_reallocate_person(self):
    # #     pass

    # def test_print_allocations(self):
    #     self.amity.print_allocations(self, *args)
    #     self.assertEqual(type(self.amity.self.print_allocations.office_occupants) > list)
    #     self.assertEqual(len(self.amity.self.print_allocations.living_occupants) > 1)


    # # def test_print_room(self):
    # #     pass

    # # def test_print_unallocated(self):
    # #     pass

    # def test_load_state(self):
    #     self.assertGreater(len(self.amity.load_state.room_state), 1)
    #     self.assertGreater(len(self.amity.load_state.living_state), 1)
    def tearDown(self):
        self.amity = None
        self.conn.close()


if __name__ == '__main__':
    unittest.main()
