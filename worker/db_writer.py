import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

class DatabaseWriter:
    def __init__(self):
        user = os.getenv("POSTGRES_USER", "user")
        password = os.getenv("POSTGRES_PASSWORD", "password")
        db_name = os.getenv("POSTGRES_DB", "observability")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

db_writer = DatabaseWriter()
