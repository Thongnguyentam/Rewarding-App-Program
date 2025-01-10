from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from constant.config import DB_CONNECTION_URL


# connection to the database
# The engine object manages the connections to the database.
engine = create_engine(DB_CONNECTION_URL)

# creating new database sessions. Disables automatic commits, automatic flushing of the session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# All SQLAlchemy models (database tables) in application will inherit from this Base class. 
# It helps SQLAlchemy map Python classes to database tables.
Base = declarative_base()

# dependency function
# provides a database session (db) to endpoints that require interaction with the database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

