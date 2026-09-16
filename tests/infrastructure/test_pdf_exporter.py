import os
import pytest
from datetime import date, datetime
from citadel.core.models.patient import Patient
from citadel.core.models.enums import BiologicalSex, ResultStatus, ResultSource
from citadel.core.models.sample import Sample
from citadel.core.models.result import Result
from citadel.infrastructure.reporting.pdf_exporter import PdfReportExporter
from citadel.application.report_service import ReportService
from citadel.core.exceptions import DomainException
from unittest.mock import MagicMock

def test_generate_patient_report(tmp_path):
    patient = Patient(1, "123", "John", "Doe", date(1980, 1, 1), BiologicalSex.MALE, None, None, datetime.now())
    sample = Sample(1, 1, "BC-123", "BLOOD", "EDTA", datetime.now(), None)
    result = Result(1, 1, 1, "105.0", ResultSource.ANALYZER, "A1", ResultStatus.VALIDATED, False, datetime.now(), 1, datetime.now())
    
    output_path = os.path.join(tmp_path, "report.pdf")
    
    exporter = PdfReportExporter()
    res_path = exporter.generate_patient_report(patient, sample, [result], output_path)
    
    assert os.path.exists(res_path)
    assert os.path.getsize(res_path) > 0
    with open(res_path, "rb") as f:
        header = f.read(4)
        assert header == b"%PDF"

def test_report_service_rejects_pending_results():
    session = MagicMock()
    sample_repo = MagicMock()
    patient_repo = MagicMock()
    result_repo = MagicMock()
    exporter = MagicMock()
    
    service = ReportService(session, sample_repo, patient_repo, result_repo, exporter)
    
    sample_repo.get_by_id.return_value = Sample(1, 1, "BC-123", "BLOOD", "EDTA", datetime.now(), None)
    session.get.return_value = MagicMock(patient_id=1)
    patient_repo.get_by_id.return_value = Patient(1, "123", "John", "Doe", date(1980, 1, 1), BiologicalSex.MALE, None, None, datetime.now())
    
    pending_res = MagicMock()
    pending_res.to_domain.return_value = Result(1, 1, 1, "105.0", ResultSource.ANALYZER, "A1", ResultStatus.PENDING, False, None, None, None)
    session.exec().all.return_value = [pending_res]
    
    with pytest.raises(DomainException, match="VALIDATED before exporting"):
        service.build_pdf_report(1, "/tmp")
