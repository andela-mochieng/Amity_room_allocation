import unittest
from ..app import Amity
import sqlite3
import ipdb

conn = sqlite3.connect("amity.sqlite")
connection = conn.cursor()


class roomstest(unittest.TestCase):
    def setUp(self):

        self.amity = Amity()

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
        ipdb.set_trace()
        self.amity.add_person(['Margie'], ['Rain'], ['Fellow]', ['Y']])
        self.name = ['Margie'] + " " + ['Rain']
        self.assertEqual(self.name, 'Margie Rain')
        self.assertTrue(self.person_type, 'Fellow')
        self.assertTrue(self.want_accommodation, 'Y')
        self.assertEqual(self.person_data, {'Fellow': {'Margie Rain': 'Y'} ,'Staff':[]})
        self.assertEqual(len(self.person_data['Staff']), 0)

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
