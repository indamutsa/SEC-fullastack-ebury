import unittest, csv, os
from unittest.mock import patch
from main import fetch_random_users, process_users, write_to_csv

class TestMain(unittest.TestCase):
    @patch('main.requests.get')
    def test_fetch_random_users(self, mock_get):
        # Mock the response from the API
        mock_data = {
            'results': [
                {'name': {'first': 'John', 'last': 'Doe'}},
                {'name': {'first': 'Jane', 'last': 'Smith'}}
            ]
        }
        mock_get.return_value.json.return_value = mock_data

        # Call the function
        users = fetch_random_users()

        # Assert the expected results
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['name']['first'], 'John')
        self.assertEqual(users[0]['name']['last'], 'Doe')
        self.assertEqual(users[1]['name']['first'], 'Jane')
        self.assertEqual(users[1]['name']['last'], 'Smith')


    def test_process_users(self):
        # Define the input data
        users = [
            {
                'name': {'first': 'John', 'last': 'Doe'},
                'login': {'username': 'johndoe'},
                'email': 'john.doe@example.com',
                'phone': '1234567890',
                'location': {'city': 'New York', 'country': 'USA'}
            },
            {
                'name': {'first': 'Jane', 'last': 'Smith'},
                'login': {'username': 'janesmith'},
                'email': 'jane.smith@example.com',
                'phone': '0987654321',
                'location': {'city': 'London', 'country': 'UK'}
            }
        ]

        # Call the function
        processed_users = process_users(users)

        # Assert the expected results
        self.assertEqual(len(processed_users), 2)
        self.assertEqual(processed_users[0]['name'], 'John Doe')
        self.assertEqual(processed_users[0]['username'], 'johndoe')
        self.assertEqual(processed_users[0]['email'], 'john.doe@example.com')
        self.assertEqual(processed_users[0]['phone'], '1234567890')
        self.assertEqual(processed_users[0]['city'], 'New York')
        self.assertEqual(processed_users[0]['country'], 'USA')
        self.assertEqual(processed_users[1]['name'], 'Jane Smith')
        self.assertEqual(processed_users[1]['username'], 'janesmith')
        self.assertEqual(processed_users[1]['email'], 'jane.smith@example.com')
        self.assertEqual(processed_users[1]['phone'], '0987654321')
        self.assertEqual(processed_users[1]['city'], 'London')
        self.assertEqual(processed_users[1]['country'], 'UK')

class TestCsvWriting(unittest.TestCase):
    def setUp(self):
        """Setup before each test method."""
        self.filename = "solutions/results-test.csv"
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def tearDown(self):
        """Clean up after each test method."""
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass  # In case the file was not created, ignore

    def test_write_to_csv_creates_correct_file_contents(self):
        # Define the input data
        users = [
            {'name': 'John Doe', 'username': 'johndoe', 'email': 'john.doe@example.com', 'phone': '1234567890', 'city': 'New York', 'country': 'USA'},
            {'name': 'Jane Smith', 'username': 'janesmith', 'email': 'jane.smith@example.com', 'phone': '0987654321', 'city': 'London', 'country': 'UK'}
        ]

        # Call the function
        write_to_csv(users, self.filename)

        # Check if the file was created and contains the correct data
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 2)
            self.assertDictEqual(rows[0], users[0])
            self.assertDictEqual(rows[1], users[1])
            self.assertEqual(rows[0]['name'], 'John Doe')
            self.assertEqual(rows[0]['username'], 'johndoe')
            self.assertEqual(rows[0]['email'], 'john.doe@example.com')
            self.assertEqual(rows[0]['phone'], '1234567890')
            self.assertEqual(rows[0]['city'], 'New York')
            self.assertEqual(rows[0]['country'], 'USA')
            self.assertEqual(rows[1]['name'], 'Jane Smith')
            self.assertEqual(rows[1]['username'], 'janesmith')
            self.assertEqual(rows[1]['email'], 'jane.smith@example.com')
            self.assertEqual(rows[1]['phone'], '0987654321')
            self.assertEqual(rows[1]['city'], 'London')
            self.assertEqual(rows[1]['country'], 'UK')


if __name__ == '__main__':
    unittest.main()