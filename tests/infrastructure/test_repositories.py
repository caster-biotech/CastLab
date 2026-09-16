import pytest
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from citadel.core.models.patient import Patient
from citadel.core.models.enums import BiologicalSex
from citadel.infrastructure.repositories.patient_repository import SqlPatientRepository

def test_patient_crud(session):
    repo = SqlPatientRepository(session)
    
    patient = Patient(
        patient_id=None,
        national_id="ID123",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 1),
        sex=BiologicalSex.MALE,
        phone=None,
        email=None,
        created_at=datetime.now()
    )
    
    saved_patient = repo.add(patient)
    assert saved_patient.patient_id is not None
    
    fetched = repo.get_by_id(saved_patient.patient_id)
    assert fetched.national_id == "ID123"

def test_patient_unique_constraint(session):
    repo = SqlPatientRepository(session)
    
    patient1 = Patient(
        patient_id=None,
        national_id="UNIQUE_ID",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 1),
        sex=BiologicalSex.MALE,
        phone=None,
        email=None,
        created_at=datetime.now()
    )
    repo.add(patient1)
    
    patient2 = Patient(
        patient_id=None,
        national_id="UNIQUE_ID",
        first_name="Jane",
        last_name="Smith",
        birth_date=date(1990, 1, 1),
        sex=BiologicalSex.FEMALE,
        phone=None,
        email=None,
        created_at=datetime.now()
    )
    
    with pytest.raises(IntegrityError):
        repo.add(patient2)
        session.flush()
