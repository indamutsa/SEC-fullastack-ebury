from uuid import uuid4
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RSAKeys(Base):
    __tablename__ = "rsa_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), unique=True)
    private_key = Column(String(10000), unique=True, index=True)  # Increased length
    public_key = Column(String(10000), unique=True, index=True)  # Increased length
    
class AESKeys(Base):
    __tablename__ = "aes_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), unique=True)
    key = Column(String, unique=True, index=True)
    filename = Column(String, unique=True, index=True)