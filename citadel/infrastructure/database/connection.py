from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session

def create_db_engine(db_url: str = "sqlite:///citadel.db") -> Engine:
    engine = create_engine(db_url, echo=False)
    return engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__ == "sqlite3":
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def get_session(engine: Engine):
    with Session(engine) as session:
        yield session

def init_db(engine: Engine):
    SQLModel.metadata.create_all(engine)
