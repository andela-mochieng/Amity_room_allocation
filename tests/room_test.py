import unittest
from ..app import Amity
import sqlite3

conn = sqlite3.connect("amity.sqlite")
connection = conn.cursor()


class roomstest(unittest.TestCase):
    def setUp(self):
        amity = Amity()

    def test_create_rooms(self):
        ''' test whether rooms are created and saved to the dictionary'''
        amity = Amity()
        amity.create_rooms(['Lilac', 'Camelot', 'Oculus' ])
        room_type = 'L'
        self.rooms = {
        'L': ['Lilac', 'Camelot', 'Oculus'],
        'O':[]
        }
        self.assertEqual(len(self.rooms['L']), 3 )
        self.assertEqual(len(self.rooms['O']), 2)


    def test_add_person(self):
        add_person(['Margie'], ['Rain'], ['Fellow]', ['Y']])
        self.assertTrue(name, 'Margie Rain')
        self.assertTrue(person_type, 'Fellow')
        self.assertTrue(want_accommodation, 'Y')

        self.assertEqual(person_data, {'Fellow': {'Margie Rain': 'Y'} 'staff'}  )

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
