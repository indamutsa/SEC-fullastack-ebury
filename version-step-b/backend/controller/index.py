import traceback, os, uuid, fakeredis
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

# from controller import init_db
from controller import init_db
from models.index import AESKeys
from service.index import decrypt_data_at_rest, encrypt_data_at_rest, generate_rsa_key_pair
from utils.helper import delete_file, get_db, isImage, persist_data, save_file_to_disk
from starlette.config import Config
from fastapi_limiter.depends import RateLimiter
    
router = APIRouter()

# Create a redis instance
redis = fakeredis.FakeStrictRedis()
config = Config(".env")


# @router.on_event("startup")
# async def startup_event():
#     init_db()
#     redis_connection = redis.from_url("redis://localhost:6739", encoding="utf-8", decode_responses=True)
#     await FastAPILimiter.init(redis_connection)
#     print("Database(SQLite) tables created | Redis connection established")


@router.get("/shakehands", dependencies=[Depends(RateLimiter(times=2, seconds=20))])
def shakehands(request: Request):
    data = generate_rsa_key_pair()
    
    session_id = str(uuid.uuid4())
    csrf_token = str(uuid.uuid4())
    
    redis.set(session_id, "valid", ex=1800)
    redis.set(csrf_token, "valid", ex=1800)

    response = JSONResponse(content={"public_key": data["public_key"]})
    response.set_cookie(key="session_id", value=session_id, httponly=False, secure=False, samesite="Lax", max_age=1800)
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=False, secure=False, samesite="Lax", max_age=300)
    
    return response

@router.post("/upload", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_upload_file(request: Request, file: UploadFile):
    try:
        # Get the session ID and CSRF token from the request cookies
        session_id = request.cookies.get("session_id")
        csrf_token = request.cookies.get("csrf_token")
        
        # Check if the session ID and CSRF token are valid
        if not session_id or not csrf_token or not redis.get(session_id) or not redis.get(csrf_token):
            raise HTTPException(status_code=403, detail="Invalid session ID or CSRF token")
        
        print(f"File received: {file.filename}")
        # save_file_to_disk(file)
        print(f"File saved to disk: {file.size}")
        
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True) # Create the upload folder if it doesn't exist
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_location = f"{upload_folder}/{unique_filename}"
        
        if not (await isImage(file)):
            return HTTPException(status_code=400, detail="Only image files are allowed")
        
        file.file.seek(0)  # Reset the file pointer to the beginning
        data = await file.read() # Read the file content into memory in a form of bytes
        print(f"Original data size: {len(data)} bytes")

        # Encrypt the file data
        encrypted_data, key = encrypt_data_at_rest(data)
        print(f"Encrypted data size: {len(encrypted_data)} bytes")

        with open(file_location, "wb") as f:
            f.write(encrypted_data)

        # Check the size of the file after writing
        encrypted_file_size = os.path.getsize(file_location)
        print(f"Encrypted file size: {encrypted_file_size} bytes")
            
        # Now let's save the AES key and IV to the database
        persist_data(data={"key": key, "filename": unique_filename}, data_type="AESKeys")
                    
        return JSONResponse(content={"message": "File uploaded successfully", "filename": unique_filename}, status_code=201)
        
        
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {e}\n{tb}") 




@router.get("/download/{filename}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def download_file(request: Request, filename: str):
    try:
        # Get the session ID and CSRF token from the request cookies
        session_id = request.cookies.get("session_id")
        csrf_token = request.cookies.get("csrf_token")
        
        # Check if the session ID and CSRF token are valid
        if not session_id or not csrf_token or not redis.get(session_id) or not redis.get(csrf_token):
            raise HTTPException(status_code=403, detail="Invalid session ID or CSRF token")
                
        db = next(get_db())
        
        key = db.query(AESKeys).filter(AESKeys.filename == filename).first().key
        

        decrypt_file_location = decrypt_data_at_rest(filename, key,  upload_folder="uploads")
        
        server_url = config.get("SERVER_URL")  # Get the server URL from the configuration file
        
        download_link = f"{server_url}/{decrypt_file_location}"  # Construct the download link
        
        return {"message": "File decrypted successfully", "download_link": download_link}
    
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while downloading the file: {e}\n{tb}") 
    


@router.get("/delete/{filename}")
async def remove_file(filename: str,  upload_folder = "uploads"):
   
    try:
       
        # Delete the file from the database
        file_location = f"{upload_folder}/{filename}"
        delete_file(file_location)
        return JSONResponse(content={"message": "File deleted successfully"})
    except:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the file")