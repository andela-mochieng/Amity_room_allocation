import unittest
from ..app import Amity
import sqlite3
import ipdb


class roomstest(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.conn = sqlite3.connect("test_amity.sqlite")
        self.connect = self.conn.cursor()
        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Rooms(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, type TEXT)")
        self.connect.execute(
            "CREATE TABLE IF NOT EXISTS Persons(id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Personnel_type TEXT, want_accommodation TEXT, office_accommodation TEXT , living_accomodation TEXT)")

        self.people_data = {'Staff': [],
                            'Fellow': []
                            }


    def test_create_rooms(self):
        ''' test whether rooms are created and saved to the dictionary'''
        self.amity.create_rooms(['Ruby', 'Emerald', 'Java'])
        self.rooms = {
            'L': ['Ruby', 'Emerald', 'Java'],
            'O': []
        }
        self.assertEqual(len(self.rooms['L']), 3)
        self.assertEqual(len(self.rooms['O']), 0)

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
            self.people_data['Fellow'].append({self.name: self.want_accommodation})
        self.assertTrue(
            self.people_data, {'Fellow': {'Margie Rain': 'Y'}, 'Staff': []})
        self.assertEqual(len(self.people_data['Staff']), 0)
        self.amity.allocation_rule(self.name, self.person_type, self.want_accommodation)

    def test_allocation_rule(self):
        self.amity.allocation_rule('Margie Rain', 'Fellow', 'Y')
        self.name = 'Margie Rain'
        self.person_type = 'Fellow'
        self.want_accommodation = 'Y'
        self.assertTrue(self.person_type, 'Fellow')
        self.assertTrue(self.want_accommodation, 'Y')
        self.office_name = self.connect.execute(
            "SELECT Name FROM Rooms where type = 'L'").fetchall()
        for off_name in self.office_name:
            off_name = map(lambda x: x.encode('ascii'), off_name)
            self.assertTrue(type(off_name), "Ruby")


    # def test_allocate_office(self):
    #     pass

    # def test_reallocate_person(self):
    #     pass

    # def test_print_allocations(self):
    #     pass

    # def test_print_room(self):
    #     pass

    # def test_print_unallocated(self):
    #     pass

    # def test_load_state(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
