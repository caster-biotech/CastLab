from PyQt6.QtCore import QObject, pyqtSignal
from citadel.application.patient_service import PatientService

class PatientViewModel(QObject):
    patient_loaded = pyqtSignal(object)
    patient_saved = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self, patient_service: PatientService):
        super().__init__()
        self.patient_service = patient_service

    def search_patient(self, national_id: str):
        try:
            # Note: simulating search with existing method. 
            # In a full app, a dedicated get_by_national_id should be exposed by the service.
            patient_data = {
                "national_id": national_id,
                "first_name": "Placeholder",
                "last_name": "Placeholder",
                "birth_date": "2000-01-01",
                "sex": "OTHER",
            }
            patient = self.patient_service.register_or_get_patient(patient_data)
            self.patient_loaded.emit(patient)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def save_patient(self, patient_data: dict):
        try:
            patient = self.patient_service.register_or_get_patient(patient_data)
            self.patient_saved.emit(patient)
        except Exception as e:
            self.error_occurred.emit(str(e))
