from abc import ABC, abstractmethod
from citadel.core.models.patient import Patient
from citadel.core.models.sample import Sample
from citadel.core.models.result import Result

class ReportExporterPort(ABC):
    @abstractmethod
    def generate_patient_report(self, patient: Patient, sample: Sample, results: list[Result], output_path: str) -> str:
        pass
