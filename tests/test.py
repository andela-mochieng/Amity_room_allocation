# import unittest
# from ..amity import *


# class AmityTests(unittest.TestCase):
#     """test of function in amity"""

#     def test_create_rooms(self):
#         spaces = create_rooms()

#         self.conn = sqlite3.connect("amity.sqlite")
#         self.connection = conn.cursor()
#         len_before_insert = spaces.
#         # self.assertIsInstance(spaces.room, data_type(['1', '3', '4']),
#         #                       msg="room type is list")
#         # self.assertEqual(room_type, "O" or "L",
#         #                  msg="room_type is either O or L")
#         # self.assertIsInstance(rooms, data_type({1: 'a', 2: 'b'}),
#         #                       msg="room type is a dictionary")
#         # self.assertEqual(key.upper(), "O" or "L",
#         #                  msg="room_type is either Office or Living space")


# if __name__ == '__main__':
#     unittest.main()
# def test_rooms_with_occupatants(self):
#         """Tests whether function returns correct number of
#         rooms with occupants"""

#         rooms = Rooms.Rooms()
#         # get number of rooms before insert
#         num_before_insert = rooms.get_rooms_with_occupants()
#         self.db = DatabaseManager("Amity.sqlite")
#         # insert record to increase number of available rooms
#         self.db.query(
#             "INSERT into Rooms (Name, Maxppl, Curppl, Room_type) VALUES('TestRoom','4','2','OFFICE')")
#         # get number of rooms after insert
#         num_after_insert = rooms.get_rooms_with_occupants()
#         # compare whether the number of available rooms increased
#         self.assertGreater(num_after_insert, num_before_insert)
