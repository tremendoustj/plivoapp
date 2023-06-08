import unittest
from app.models import Message

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.account_id = '12345'
        self.message_id = 'abcde'
        self.sender_number = '1111111111'
        self.receiver_number = '2222222222'
    
    def tearDown(self):
        # Clean up database after each test
        Message.query.delete()

    def test_message_save(self):
        # Create a test message
        message = Message(
            id=self.message_id,
            account_id=self.account_id,
            sender_number=self.sender_number,
            receiver_number=self.receiver_number
        )
        message.save()

        # Check if the message is saved in the database
        saved_message = Message.query.filter_by(id=self.message_id).first()
        self.assertIsNotNone(saved_message)
        self.assertEqual(saved_message.account_id, self.account_id)
        self.assertEqual(saved_message.sender_number, self.sender_number)
        self.assertEqual(saved_message.receiver_number, self.receiver_number)
    
    def test_message_delete(self):
        # Create a test message
        message = Message(
            id=self.message_id,
            account_id=self.account_id,
            sender_number=self.sender_number,
            receiver_number=self.receiver_number
        )
        message.save()

        # Delete the message from the database
        message.delete()

        # Check if the message is deleted
        deleted_message = Message.query.filter_by(id=self.message_id).first()
        self.assertIsNone(deleted_message)

if __name__ == '__main__':
    unittest.main()
