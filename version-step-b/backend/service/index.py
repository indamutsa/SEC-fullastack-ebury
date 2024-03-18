import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

# from fastapi import Depends
from sqlalchemy.orm import Session
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import b64decode
from base64 import b64encode

from models.index import AESKeys
from utils.helper import get_db, persist_data


def generate_rsa_key_pair(db: Session = next(get_db())):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Generate public key
    public_key = private_key.public_key()

    # Serialize private key
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Decode the keys to strings before inserting them into the database
    data = {"pem": pem.decode('utf-8'), "pem_public": pem_public.decode('utf-8')}
    db_rsa_key = persist_data(data, "RSAKeys", db)

    return {"id": db_rsa_key.id, "private_key": db_rsa_key.private_key, "public_key": db_rsa_key.public_key}


def encrypt_data_at_rest(data: bytes):
    # Generate a random 32-byte key for AES encryption
    key = get_random_bytes(16)
    
    # Create a new AES cipher object with the key and AES.MODE_CBC mode
    cipher = AES.new(key, AES.MODE_CBC)
    
    iv = cipher.iv # Initialization Vector
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    # The encrypted data is prefixed with the IV then written to the file
    file_data = iv + encrypted_data

    return file_data, b64encode(key).decode('utf-8')

def decrypt_data_at_rest(filename: str, key: str, db: Session = next(get_db()), upload_folder = "uploads"):
    # Decrypt the data
    try:    
        file_location = f"{upload_folder}/{filename}"
        file_size = os.path.getsize(file_location) 
        print(f"---> file size: {file_size} bytes")
        # Query the database for the AES key
        # aes_key = db.query(AESKeys).filter(AESKeys.filename == filename).first()
        # print("----------------------->>>>>>>>>>>>>>", aes_key)

        
        # Read the encrypted file
        with open(file_location, "rb") as f:
            encrypted_data = f.read()
            
        # Decode the key from base64
        key = b64decode(key)
        
        # Get the IV from the first 16 bytes of the encrypted file
        iv = encrypted_data[:16]
        
        # Get the rest of the encrypted data
        encrypted_data = encrypted_data[16:]
        print(f"Encrypted data size (without IV): {len(encrypted_data)} bytes")
        
        # Create a new AES cipher object with the key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        
        # Decrypt the data
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        # Write the decrypted data to a new file
        decrypted_file_location = f"{upload_folder}/decrypted_{filename}"
        
        with open(decrypted_file_location, "wb") as f:
            f.write(decrypted_data)
            
        # The size of the decrypted file in bytes
        decrypted_file_size = os.path.getsize(decrypted_file_location) 
        print(f"Decrypted file size: {decrypted_file_size} bytes")
        
        return decrypted_file_location
    except ValueError as e:
        print(f"Error during decryption: {e}")
        decrypted_data = b""    