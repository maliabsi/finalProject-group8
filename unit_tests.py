import unittest
from unittest.mock import MagicMock, patch
from stytch_tools import stytch_auth, get_user_data


class stytch_test(unittest.TestCase):
    def test_none_integer_case(self):
        test_value = MagicMock(status_code=500)
        expected_output = None
        with patch("stytch_tools.client.oauth.authenticate") as mock_get:
            mock_get.return_value = test_value
            actual_output = stytch_auth(test_value)[0]
            self.assertEqual(expected_output, actual_output)

    def test_none_string_case(self):
        test_value = MagicMock(status_code="404 not found")
        expected_output = None
        with patch("stytch_tools.client.oauth.authenticate") as mock_get:
            mock_get.return_value = test_value
            actual_output = stytch_auth(test_value)[0]
            self.assertEqual(expected_output, actual_output)

    def test_success_case(self):
        test_value = MagicMock(status_code=200)
        expected_output = True
        with patch("stytch_tools.client.oauth.authenticate") as mock_get:
            with patch("stytch_tools.json.loads") as mock_post:
                mock_post = "post_value"
                mock_get.return_value = test_value
                actual_output = stytch_auth(test_value)[1]
                self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":  # this is the last line
    unittest.main()
