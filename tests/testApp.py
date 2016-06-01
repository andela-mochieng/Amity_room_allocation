import unittest
import sqlite3
import os
from ..main.app import Amity, welcome_msg
from ..main.models.person import Person, Fellow, Staff
from ..main.models.room import Office, LivingSpace
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
        ''' Test if person is added '''
        self.amity.add_person("Margie", "Rain", "Fellow", "Y")
        self.amity.add_person("Chidi", "Nnadi", "Staff", 'N')
        self.amity.add_person("Margie", "Akoth", "Fellow", "N")
        self.assertEqual(len(self.amity.people['fellow to house']), 1)
        self.assertEqual(len(self.amity.people['staff and fellow']), 2)
        self.assertEqual(self.amity.rooms, {'L': {}, 'O': {}})
        # person = Person.create_person("Margie Rain", "Fellow", "Y")
        # ipdb.set_trace()
        # self.amity.allocate_room(person, 'L')
        # print self.amity.rooms



    def test_allocate_room(self):

        room_type = 'O' or 'L'
        self.assertEqual(len(self.amity.unallocated[room_type]), 0)
        self.assertEqual(self.amity.rooms, {'L': {}, 'O': {}})



    def test_print_unallocated(self):
        """
        Test that unallocated people are displayed on screen
        and printed to a text file if specified
        """
        person = "Chadi Rain", "Fellow", "Y"
        self.amity.unallocated['L'].append(person)
        self.amity.print_unallocated("unallocated.txt")

        # Data entry
        with open("unallocated.txt", 'a+') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
        self.assertTrue(os.path.exists("unallocated.txt"))
        os.remove("unallocated.txt")


    def tearDown(self):
        self.amity = None


if __name__ == '__main__':
    unittest.main()
