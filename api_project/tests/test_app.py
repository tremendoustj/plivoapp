import unittest
from flask import jsonify
from unittest.mock import patch
from app import app
from app.models import Message

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.account_id = '12345'
        self.message_id = 'abcde'
        self.sender_number = '1111111111'
        self.receiver_number = '2222222222'
    
    def tearDown(self):
        # Clean up database after each test
        with app.app_context():
            Message.query.delete()
    
    def test_get_messages(self):
        # Create a test message
        message = Message(
            id=self.message_id,
            account_id=self.account_id,
            sender_number=self.sender_number,
            receiver_number=self.receiver_number
        )
        with app.app_context():
            message.save()

        # Make a GET request to /messages/<account_id>
        response = self.app.get(f'/messages/{self.account_id}')
        data = response.get_json()

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['account_id'], self.account_id)
        self.assertEqual(data[0]['message_id'], self.message_id)
        self.assertEqual(data[0]['sender_number'], self.sender_number)
        self.assertEqual(data[0]['receiver_number'], self.receiver_number)
    
    def test_create_message(self):
        # Make a POST request to /create with message data
        data = {
            'message_id': self.message_id,
            'account_id': self.account_id,
            'sender_number': self.sender_number,
            'receiver_number': self.receiver_number
        }
        response = self.app.post('/create', json=data)
        data = response.get_json()

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Message created successfully')

        # Check if the message is saved in the database
        with app.app_context():
            message = Message.query.filter_by(id=self.message_id).first()
            self.assertIsNotNone(message)
            self.assertEqual(message.account_id, self.account_id)
            self.assertEqual(message.sender_number, self.sender_number)
            self.assertEqual(message.receiver_number, self.receiver_number)
    
    def test_search_messages(self):
        # Create test messages
        message1 = Message(
            id='message1',
            account_id=self.account_id,
            sender_number=self.sender_number,
            receiver_number='3333333333'
        )
        message2 = Message(
            id='message2',
            account_id=self.account_id,
            sender_number='4444444444',
            receiver_number=self.receiver_number
        )
        with app.app_context():
            message1.save()
            message2.save()

        # Make a GET request to /search with filter parameters
        response = self.app.get(f'/search?sender_number={self.sender_number}')
        data = response.get_json()

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['account_id'], self.account_id)
        self.assertEqual(data[0]['message_id'], 'message1')
        self.assertEqual(data[0]['sender_number'], self.sender_number)
        self.assertEqual(data[0]['receiver_number'], '3333333333')
        self.assertEqual(data[1]['account_id'], self.account_id)
        self.assertEqual(data[1]['message_id'], 'message2')
        self.assertEqual(data[1]['sender_number'], '4444444444')
        self.assertEqual(data[1]['receiver_number'], self.receiver_number)

if __name__ == '__main__':
    unittest.main()
