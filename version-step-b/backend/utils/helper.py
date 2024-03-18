import imghdr, os
import uuid
from sqlalchemy.orm import Session
from models.index import AESKeys, RSAKeys, SessionLocal

# Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def persist_data(data, data_type, db: Session = next(get_db())):
    
    match data_type:
        case "RSAKeys":
            pem = data['pem']
            pem_public = data['pem_public']
                        
            db_rsa_key = RSAKeys(private_key=pem, public_key=pem_public)
            db.add(db_rsa_key)  # Add the RSAKeys instance, not the data dictionary
            db.commit()
            db.refresh(db_rsa_key)  # Refresh the RSAKeys instance, not the data dictionary
            
            return db_rsa_key

        
        case "AESKeys":
            db_aes = AESKeys(key=data['key'], filename=data['filename'])
            
            db.add(db_aes)  # Add the AESKeys instance, not the data dictionary
            db.commit()
            db.refresh(db_aes)  # Refresh the AESKeys instance, not the data dictionary
            
            return db_aes
    
async def isImage(file):
    data = await file.read()
    file_type = imghdr.what(None, data)
    _, file_extension = os.path.splitext(file.filename)
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    
    return True if file_type and file_extension in allowed_extensions else False

def delete_file(file_path, db: Session = next(get_db()), upload_folder: str = "uploads"):
    # Extract the filename from the file path / filename
    filename = file_path.split("/")[-1]
    
    file_path_ = f"{upload_folder}/{filename}"
    try:
        db.query(AESKeys).filter(AESKeys.filename == filename).delete()
        os.remove(file_path) if os.path.exists(file_path) else None
        os.remove(file_path_) if os.path.exists(file_path_) else None
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
    return True

def save_file_to_disk(file, upload_folder: str = "uploads"):
    # Generate a unique filename
    filename = str(uuid.uuid4())

    # Save the file to disk
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return file_path
