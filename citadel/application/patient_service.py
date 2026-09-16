from sqlmodel import Session, select
from citadel.core.models.patient import Patient
from citadel.infrastructure.database.models import PatientModel
from citadel.infrastructure.repositories.patient_repository import SqlPatientRepository

class PatientService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = SqlPatientRepository(session)

    def register_or_get_patient(self, patient_data: dict) -> Patient:
        try:
            stmt = select(PatientModel).where(PatientModel.national_id == patient_data.get("national_id"))
            existing_model = self.session.exec(stmt).first()
            if existing_model:
                return existing_model.to_domain()
            
            patient = Patient(
                patient_id=None, # type: ignore
                national_id=patient_data["national_id"],
                first_name=patient_data["first_name"],
                last_name=patient_data["last_name"],
                birth_date=patient_data["birth_date"],
                sex=patient_data["sex"],
                phone=patient_data.get("phone"),
                email=patient_data.get("email"),
                created_at=patient_data.get("created_at")
            )
            saved = self.repo.add(patient)
            self.session.commit()
            return saved
        except Exception:
            self.session.rollback()
            raise
