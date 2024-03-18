import asyncio
import unittest, os
from unittest.mock import MagicMock
from unittest.mock import patch, AsyncMock
from models.index import AESKeys, RSAKeys
from utils.helper import isImage, persist_data, delete_file

class HelperTests(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.upload_folder = "uploads/test"

    def test_persist_data_rsa_keys(self):
        data = {
            'pem': 'private_key',
            'pem_public': 'public_key'
        }
        data_type = 'RSAKeys'

        result = persist_data(data, data_type, self.db)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertIsInstance(result, RSAKeys)

    def test_persist_data_aes_keys(self):
        data = {
            'key': 'encryption_key',
            'iv': 'initialization_vector',
            'filename': 'file.txt'
        }
        data_type = 'AESKeys'

        result = persist_data(data, data_type, self.db)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertIsInstance(result, AESKeys)

    def test_delete_file(self):
        filename = "test_file.txt"
        
        # Write to the file
        with open(f"{self.upload_folder}/{filename}", "w") as f:
            f.write("This is a test file")
        
        self.db.query.return_value.filter.return_value.delete.return_value = None
        os.path.exists.side_effect = [True, True]

        with patch("os.remove") as mock_remove:
            delete_file(filename, self.db, self.upload_folder)

            self.db.query.assert_called_once_with(AESKeys)
            self.db.query.return_value.filter.return_value.delete.assert_called_once()
            mock_remove.assert_called_with(f"{self.upload_folder}/{filename}")

    @patch('imghdr.what')
    def test_isImage(self, mock_imghdr):
        # Mock the file object
        mock_file = AsyncMock()
        mock_file.filename = 'test.png'
        mock_file.read.return_value = b'test data'

        # Mock the imghdr.what function to return 'png'
        mock_imghdr.return_value = 'png'

        # Call the function with the mock file
        result = asyncio.run(isImage(mock_file))

        # Assert that the function returned True
        self.assertTrue(result)

        # Now test with a non-image file
        mock_file.filename = 'test.txt'
        mock_imghdr.return_value = None

        # Call the function with the mock file
        result = asyncio.run(isImage(mock_file))

        # Assert that the function returned False
        self.assertFalse(result)            

if __name__ == '__main__':
    unittest.main()