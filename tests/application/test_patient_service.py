from datetime import date, datetime
from citadel.application.patient_service import PatientService
from citadel.core.models.enums import BiologicalSex

def test_register_or_get_patient(session):
    service = PatientService(session)
    data = {
        "national_id": "NAT-1",
        "first_name": "Test",
        "last_name": "User",
        "birth_date": date(1980, 1, 1),
        "sex": BiologicalSex.MALE,
        "created_at": datetime.now()
    }
    
    patient1 = service.register_or_get_patient(data)
    assert patient1.patient_id is not None
    
    patient2 = service.register_or_get_patient(data)
    assert patient2.patient_id == patient1.patient_id
