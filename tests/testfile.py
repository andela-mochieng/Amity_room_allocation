import unittest
from ..main.util import File
import os
import ipdb
class fileParserTest(unittest.TestCase):


    def test_read_file(self):
        '''Test reading files.'''

        parser = File.FileParser(
        os.path.dirname(os.path.realpath("testData.txt")) + "/tests/testData.txt")
        parser.read_file()
        self.assertEqual(len(parser.allocations_list), 3)

        self.assertEqual(parser.allocations_list[0], ['PEGGIE WANJIRU', 'FELLOW', 'Y'])



if __name__ == '__main__':
    unittest.main()
