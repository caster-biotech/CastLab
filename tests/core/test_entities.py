from datetime import date, datetime
import pytest

from citadel.core.models.patient import Patient
from citadel.core.models.enums import BiologicalSex

def test_patient_age_calculation():
    birth_date = date(1990, 1, 1)
    patient = Patient(
        patient_id=1,
        national_id="123456789",
        first_name="John",
        last_name="Doe",
        birth_date=birth_date,
        sex=BiologicalSex.MALE,
        phone=None,
        email=None,
        created_at=datetime.now()
    )
    
    today = datetime.now().date()
    expected_days = (today - birth_date).days
    
    assert patient.age_in_days == expected_days
    
    expected_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    assert patient.age_in_years == expected_years
