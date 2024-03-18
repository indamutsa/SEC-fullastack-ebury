import unittest

from unittest.mock import patch, MagicMock, create_autospec
from sqlalchemy.orm import Session
from controller import SessionLocal
from service.index import decrypt_data_at_rest, encrypt_data_at_rest, generate_rsa_key_pair
import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from utils.helper import delete_file, persist_data, get_db


from base64 import b64encode
import os

from utils.helper import get_db

class TestEncryption(unittest.TestCase):
    def setUp(self):
        # self.data = b"This is some test data"
        with open("uploads/test/image.png", "rb") as f:
            self.data = f.read()
            
        # self.filename = "test_file.txt"
        self.filename = "image_test.png"
        self.upload_folder = "uploads/test"
        os.makedirs(self.upload_folder, exist_ok=True)
        self.db = MagicMock()

    def test_encryption_decryption(self):
        # Encrypt the data
        encrypted_data, key = encrypt_data_at_rest(self.data)

        # Write the encrypted data to a file
        with open(f"{self.upload_folder}/{self.filename}", "wb") as f:
            f.write(encrypted_data)

        # Decrypt the data
        decrypted_file_location = decrypt_data_at_rest(self.filename, key, upload_folder=self.upload_folder)

        # Read the decrypted data
        with open(decrypted_file_location, "rb") as f:
            decrypted_data = f.read()

        # Check if the decrypted data matches the original data
        self.assertEqual(decrypted_data, self.data)
        delete_file(self.filename, upload_folder = self.upload_folder)
        delete_file(decrypted_file_location)

    
    @patch('utils.helper.persist_data')
    @patch('controller.SessionLocal', return_value=create_autospec(Session))
    def test_generate_rsa_key_pair(self, mock_session_local, mock_persist_data):
        db_mock = MagicMock(id=1, private_key='private_key', public_key='public_key')
        mock_persist_data.return_value = db_mock

        # Act
        result = generate_rsa_key_pair(db=mock_session_local())

        # Assert
        self.assertIsNotNone(result["public_key"])
        self.assertIsNotNone(result["private_key"])
        mock_session_local().close()
        mock_session_local().close.assert_called_once()
    
        
        

if __name__ == '__main__':
    unittest.main()