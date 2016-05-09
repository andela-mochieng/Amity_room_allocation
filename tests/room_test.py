import unittest
from .. app import *
import sqlite3
from run import Amity
conn = sqlite3.connect("amity.sqlite")
connection = conn.cursor()


class roomstest(unittest.TestCase):
    def test_create_rooms(self):
        # test whether rooms ares created and saved to the db
        amity = Amity()

        args = {'<room_name>': ['lilac', 'shell']}
        amity.do_create_rooms(args)
    #     room.room_type = 'O' or 'L'
    #     room.rooms = {room.room_type: room.room_list}
    #     self.assertEqual(type(room.rooms), args)

    # def test_add_person(self):
    #     args = {'<person_fname>': 'andrew',
    #             '<person_lname>': 'mutembei', 'FELLOW': 'fellow', '--wa': 'y'}
    #     person = add_person(args)
    #     self.assertEqual(type(person), args)

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
