import pytest
from sqlmodel import Session
from citadel.infrastructure.database.connection import create_db_engine, init_db
from citadel.infrastructure.database.models import *

@pytest.fixture(scope="session")
def engine():
    _engine = create_db_engine("sqlite:///:memory:")
    init_db(_engine)
    return _engine

@pytest.fixture(scope="function")
def session(engine):
    with Session(engine) as session:
        yield session
