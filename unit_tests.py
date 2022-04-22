# pylint: disable=unused-variable
"""
Unit Tests for the app.
"""
import unittest
from unittest.mock import MagicMock, patch
from stytch_tools import stytch_oauth, get_user_data, stytch_email_auth


class StytchTest(unittest.TestCase):
    """
    Tests different parts of the stytch API implementation
    """

    def test_none_integer_case(self):
        """
        Test for correct response if stytch returns a response with a status code that is not 200
        """
        test_value = MagicMock(status_code=500)
        expected_output = None
        with patch("stytch_tools.client.oauth.authenticate") as mock_get:
            mock_get.return_value = test_value
            actual_output = stytch_oauth(test_value)[0]
            self.assertEqual(expected_output, actual_output)

    def test_none_string_case(self):
        """
        Test failure if status code response is a string instead of int
        """
        test_value = MagicMock(status_code="404 not found")
        expected_output = None
        with patch("stytch_tools.client.oauth.authenticate") as mock_get:
            mock_get.return_value = test_value
            actual_output = stytch_oauth(test_value)[0]
            self.assertEqual(expected_output, actual_output)

    def test_user_return(self):
        """
        Tests that a user is returned on request to stytch db.
        """
        mock_user = MagicMock()
        mock_user.json.return_value = {
            "created_at": "2022-04-05T18:43:15Z",
            "crypto_wallets": [],
            "emails": [
                {
                    "email": "mcfralish@yahoo.com",
                    "email_id": "email-test-7bafd4b3-893e-4bc8-8a31-8a8b41605afc",
                    "verified": False,
                }
            ],
            "name": {
                "first_name": "Michael",
                "last_name": "Fralish",
                "middle_name": "",
            },
            "phone_numbers": [],
            "providers": [
                {"provider_subject": "10228086012278278", "provider_type": "Facebook"}
            ],
            "request_id": "request-id-test-87f5b438-3261-4425-9c78-90734afb3103",
            "status": "active",
            "status_code": 200,
            "totps": [],
            "user_id": "user-test-552d704c-39b0-4c02-a0a1-f9d71a7473d9",
            "webauthn_registrations": [],
        }

        with patch("stytch_tools.client.users.get") as mock_get:
            with patch("stytch_tools.json.loads") as dummy_return:
                mock_get.return_value = mock_user
                dummy_return = "12345"
                actual_output = get_user_data(mock_user)[1]
                expected_output = True
                self.assertEqual(expected_output, actual_output)

    def test_success_case(self):
        """
        Tests if authentication was a success
        """
        test_value = MagicMock(status_code=200)
        expected_output = True
        with patch("stytch_tools.client.oauth.authenticate") as mock_get:
            with patch("stytch_tools.json.loads") as mock_post:
                mock_get.return_value = test_value
                actual_output = stytch_oauth(test_value)[1]
                self.assertEqual(expected_output, actual_output)

    def test_email_auth(self):
        """
        Tests if email authentication was a success
        """
        test_value = MagicMock(status_code=200)
        expected_output = True
        with patch("stytch_tools.client.magic_links.authenticate") as mock_get:
            with patch("stytch_tools.json.loads") as mock_post:
                mock_get.return_value = test_value
                actual_output = stytch_email_auth(test_value)[1]
                self.assertEqual(expected_output, actual_output)

    def test_email_auth_fail_case(self):
        """
        Tests if email authentication will fail
        """
        test_value = MagicMock(status_code=500)
        expected_output = None
        with patch("stytch_tools.client.magic_links.authenticate") as mock_get:
            with patch("stytch_tools.json.loads") as mock_post:
                mock_get.return_value = test_value
                actual_output = stytch_email_auth(test_value)[1]
                self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":  # this is the last line
    unittest.main()
