from PyQt6.QtCore import QObject, pyqtSignal
from citadel.application.worksheet_service import WorksheetService

class WorksheetViewModel(QObject):
    batch_processed = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, worksheet_service: WorksheetService):
        super().__init__()
        self.worksheet_service = worksheet_service

    def submit_batch_results(self, results_data: list[dict], user_id: int):
        try:
            processed = self.worksheet_service.process_bulk_results(results_data, user_id)
            self.batch_processed.emit(processed)
        except Exception as e:
            self.error_occurred.emit(str(e))
