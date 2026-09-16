import os
from sqlmodel import Session, select
from citadel.infrastructure.database.models import OrderModel, SampleModel, ResultModel
from citadel.core.ports.repositories import SampleRepository, PatientRepository, ResultRepository
from citadel.core.ports.report_exporter import ReportExporterPort
from citadel.core.exceptions import DomainException
from citadel.core.models.enums import ResultStatus

class ReportService:
    def __init__(self, session: Session, sample_repo: SampleRepository, patient_repo: PatientRepository, result_repo: ResultRepository, exporter: ReportExporterPort):
        self.session = session
        self.sample_repo = sample_repo
        self.patient_repo = patient_repo
        self.result_repo = result_repo
        self.exporter = exporter

    def get_patient_history(self, patient_id: int) -> list[dict]:
        try:
            stmt = select(OrderModel, SampleModel, ResultModel)\
                .join(SampleModel, OrderModel.order_id == SampleModel.order_id)\
                .join(ResultModel, SampleModel.sample_id == ResultModel.sample_id)\
                .where(OrderModel.patient_id == patient_id)
                
            results = self.session.exec(stmt).all()
            
            history = []
            for order, sample, result in results:
                history.append({
                    "order_id": order.order_id,
                    "sample_id": sample.sample_id,
                    "result_id": result.result_id,
                    "test_id": result.test_id,
                    "obtained_value": result.obtained_value,
                    "status": result.status
                })
            return history
        except Exception:
            self.session.rollback()
            raise

    def build_pdf_report(self, sample_id: int, output_dir: str) -> str:
        try:
            sample = self.sample_repo.get_by_id(sample_id)
            if not sample:
                raise DomainException(f"Sample {sample_id} not found")
                
            order_model = self.session.get(OrderModel, sample.order_id)
            if not order_model:
                raise DomainException("Order not found")
            patient = self.patient_repo.get_by_id(order_model.patient_id)
            if not patient:
                raise DomainException("Patient not found")
                
            stmt = select(ResultModel).where(ResultModel.sample_id == sample_id)
            result_models = self.session.exec(stmt).all()
            results = [rm.to_domain() for rm in result_models]
            
            if not results:
                raise DomainException("No results found for sample")
                
            for res in results:
                if res.status != ResultStatus.VALIDATED:
                    raise DomainException("All results must be VALIDATED before exporting report")
                    
            output_path = os.path.join(output_dir, f"report_sample_{sample_id}.pdf")
            self.exporter.generate_patient_report(patient, sample, results, output_path)
            return output_path
            
        except Exception:
            self.session.rollback()
            raise
