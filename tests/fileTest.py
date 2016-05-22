import unittest
from .util.file import FileParser


class fileParserTest(unittest.Testcase):
    def setUp():
        self.file = FileParser()

    def test_read_file(self):
        self.file.allocations = []
        lines = [line.rstrip('\n') for line in open(self.file_path, 'r')]
        self.assertEqual(self.file, len(lines))
