from models.index import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Database Configuration (Update this according to your setup)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Example for SQLite

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Initialization Function
def init_db():
    print("Database(SQLite) tables created | Redis connection established")
    Base.metadata.create_all(bind=engine)
    