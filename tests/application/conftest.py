import pytest
from datetime import date, datetime
from sqlmodel import Session, select
from citadel.infrastructure.database.connection import create_db_engine, init_db
from citadel.infrastructure.database.models import UserModel, TestCatalogModel
from citadel.core.models.enums import UserRole

@pytest.fixture(scope="session")
def engine():
    _engine = create_db_engine("sqlite:///:memory:")
    init_db(_engine)
    return _engine

@pytest.fixture(scope="function")
def session(engine):
    with Session(engine) as session:
        if not session.exec(select(UserModel).where(UserModel.username == "bio")).first():
            bio_user = UserModel(
                username="bio", password_hash="h", full_name="Bio", role=UserRole.BIOANALIST, created_at=datetime.now()
            )
            session.add(bio_user)
            
        if not session.exec(select(UserModel).where(UserModel.username == "asst")).first():
            asst_user = UserModel(
                username="asst", password_hash="h", full_name="Asst", role=UserRole.ASSISTANT, created_at=datetime.now()
            )
            session.add(asst_user)
            
        if not session.exec(select(TestCatalogModel).where(TestCatalogModel.code == "GLU")).first():
            test_cat = TestCatalogModel(
                code="GLU", name="Glucose", laboratory_area="CHEM", unit_of_measure="mg/dL", panic_min=50, panic_max=400
            )
            session.add(test_cat)
            
        session.commit()
        
        yield session
