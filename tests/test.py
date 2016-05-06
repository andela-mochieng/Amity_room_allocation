import unittest
from ..amity import Amity


class AmityTests(unittest.TestCase):
    """test of function in amity"""

    def setup(self):
        self.amity = Amity()
        self.amity.do_create_rooms()
        self.amity.conn = sqlite3.connect("amity.sqlite")
        self.amity.connection = conn.cursor()

    def test_do_create_rooms(self):
        self.assertIsInstance(spaces.room, data_type(['1', '3', '4']),
                              msg="room type is list")
        self.assertEqual(room_type, "O" or "L",
                         msg="room_type is either O or L")
        self.assertIsInstance(rooms, data_type({1: 'a', 2: 'b'}),
                              msg="room type is a dictionary")
        self.assertEqual(key.upper(), "O" or "L",
                         msg="room_type is either Office or Living space")


if __name__ == '__main__':
  unittest.main()
