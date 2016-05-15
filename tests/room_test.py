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




    def test_create_rooms(self):
        ''' test whether rooms are created and saved to the dictionary'''
        self.amity.create_rooms(['Lilac', 'Camelot', 'Oculus' ])
        room_type = 'L'
        self.rooms = {
        'L': ['Lilac', 'Camelot', 'Oculus'],
        'O':[]
        }
        self.assertEqual(len(self.rooms['L']), 3 )
        self.assertEqual(len(self.rooms['O']), 0)




    def test_add_person(self):
        self.amity.add_person('Margie', 'Rain', 'Fellow', 'Y')
        self.name = 'Margie' + " " + 'Rain'

        self.assertEqual(self.name, 'Margie Rain')
        self.person_type
        self.assertEqual(self.people_data, {'Fellow': {'Margie Rain': 'Y'} ,'Staff':[]})
        self.assertEqual(len(self.people_data['Staff']), 0)



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
