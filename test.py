import unittest
from app import app
import json
import sqlite3

class AppTestCase(unittest.TestCase):
    """
        This is the class that contains tests for each case. We have 3 scenarios mentioned below:
        1. The user enters the correct username and password. To test this, we add a dummy username and password to the 
            database and then use that as the input for the request.
        2. The user enters the incorrect username. To test this an incorrect username and password will be sent as input
            for the request.
        3. The user enters the incorrect password. To test this a dummy user is entered into the database and then the 
            correct username but incorrect password is sent as input for the request.
    """

    def setUp(self):
        """
            Function to set up the test client
        """
        self.app = app.test_client()

    def test_valid_authentication(self):
        """
            Function to test the case with correct username and password
        """
        # Create a test user in the SQLite database
        with app.app_context():
            conn = sqlite3.connect('random_people.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO people (username, password, date_of_birth, age, sex, email) VALUES (?, ?, ?, ?, ?, ?)",
                           ('testuser', 'testpassword', '2000-01-01', 25, 'Male', 'testuser@example.com'))
            conn.commit()
            conn.close()

        # Send a POST request with the correct username and password
        response = self.app.post('/get_authentication', json={'user_name': 'testuser', 'password': 'testpassword'})

        # Check if the response contains the expected data 
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['Authentication'], 'Login successful.')

    def test_invalid_username_authentication(self):
        """
            Function to test the case with incorrect username 
        """
        # Send a POST request with an incorrect username and password
        response = self.app.post('/get_authentication', json={'user_name': 'nonexistentuser', 'password': 'testpassword'})

        # Check if the response contains the expected error message
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(data['Authentication'], 'User not found. Please register.')

    def test_invalid_password_authentication(self):
        """
            Function to test the case with incorrect password
        """
        # Create a test user in the SQLite database
        with app.app_context():
            conn = sqlite3.connect('random_people.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO people (username, password, date_of_birth, age, sex, email) VALUES (?, ?, ?, ?, ?, ?)",
                           ('testuser', 'testpassword', '2000-01-01', 25, 'Male', 'testuser@example.com'))
            conn.commit()
            conn.close()

        # Send a POST request with the correct username but incorrect password
        response = self.app.post('/get_authentication', json={'user_name': 'testuser', 'password': 'wrongpassword'})

        # Check if the response contains the expected error message
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(data['Authentication'], 'Incorrect password. Please try again.')

if __name__ == '__main__':
    unittest.main()
