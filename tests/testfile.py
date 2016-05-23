import unittest
from ..main.util import File
import os

class fileParserTest(unittest.TestCase):


    def test_read_file(self):
        parser = File.FileParser(
        os.path.dirname(os.path.realpath("testData.txt")) + "/tests/testData.txt")
        list_allocations = parser.read_file()
        self.assertEqual(list_allocations, 3)




if __name__ == '__main__':
    unittest.main()
