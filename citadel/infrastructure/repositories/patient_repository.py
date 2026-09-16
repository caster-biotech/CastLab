from typing import Optional
from sqlmodel import Session
from citadel.core.ports.repositories import PatientRepository
from citadel.core.models.patient import Patient
from citadel.infrastructure.database.models import PatientModel

class SqlPatientRepository(PatientRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        model = self.session.get(PatientModel, patient_id)
        return model.to_domain() if model else None

    def add(self, patient: Patient) -> Patient:
        model = PatientModel.from_domain(patient)
        self.session.add(model)
        self.session.flush()
        return model.to_domain()
