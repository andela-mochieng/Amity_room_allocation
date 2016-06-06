import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from ..main.models.person import Person


class TestPerson(unittest.TestCase):
    """Test cases for Person class"""

    def test_fellow_input_data(self):
        person = Person.instance('Margie rain', 'Fellow', 'Y')
        self.assertEqual(person.name, 'Margie rain')
        self.assertTrue(person.living_space, True)
        self.assertTrue(person.person_type.lower(), 'fellow')

    def test_staff_details(self):
        """test that correct staff details are configured eg that living_space
        is always False"""
        person = Person.instance('Chidi Nadi', 'staff', 'N')
        self.assertEqual(person.name, 'Chidi Nadi')
        self.assertEqual(person.living_space, False)
        self.assertTrue(person.is_staff, True)

if __name__ == '__main__':
    unittest.main()
