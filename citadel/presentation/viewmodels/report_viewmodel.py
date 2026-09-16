from PyQt6.QtCore import QObject, pyqtSignal
from citadel.application.report_service import ReportService

class ReportViewModel(QObject):
    report_generated = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, report_service: ReportService):
        super().__init__()
        self.report_service = report_service

    def generate_report(self, sample_id: int, output_dir: str):
        try:
            path = self.report_service.build_pdf_report(sample_id, output_dir)
            self.report_generated.emit(path)
        except Exception as e:
            self.error_occurred.emit(str(e))
