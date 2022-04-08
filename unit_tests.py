import unittest
from unittest.mock import MagicMock, patch
from python_functions import stytch_tools


class stytch_test(unittest.TestCase):
    def test_none_case(self):
        test_value = None
        expected_output = None
        actual_output = get_movie_url(test_value)
        self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":  # this is the last line
    unittest.main()
