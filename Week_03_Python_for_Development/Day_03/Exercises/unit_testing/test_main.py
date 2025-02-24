import unittest
from main import add, is_even, API
from unittest.mock import Mock, patch


class TestAPI(unittest.TestCase):

    def setUp(self):
        base_url = "abc.example.com"
        self.obj = API(base_url)

    @patch("main.requests.get")
    def test_get_details(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Name": "Ahan", "ID": 23}
        mock_get.return_value = mock_response

        user_data = self.obj.get_details(23)
        mock_get.assert_called_with("abc.example.com/23")
        self.assertEqual(user_data, mock_response.json)


class TestMath(unittest.TestCase):

    def test_add(self):
        test_cases = [(2, 3, 5), (-1, 1, 0), (0, 0, 0)]
        for x, y, expected in test_cases:
            with self.subTest(x=x, y=y):
                self.assertEqual(add(x, y), expected)

    def testis_even(self):
        self.assertTrue(is_even(2))
        self.assertEqual(is_even(3), False)


if __name__ == "__main__":
    unittest.main()
