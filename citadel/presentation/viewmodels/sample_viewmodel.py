from PyQt6.QtCore import QObject, pyqtSignal
from citadel.application.sample_service import SampleService
from citadel.core.models.enums import OrderOrigin

class SampleViewModel(QObject):
    order_created = pyqtSignal(object, list)
    result_updated = pyqtSignal(object)
    result_validated = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(self, sample_service: SampleService):
        super().__init__()
        self.sample_service = sample_service

    def create_order(self, patient_id: int, physician: str, origin: OrderOrigin, test_ids: list[int]):
        try:
            order, samples = self.sample_service.create_order_with_samples(patient_id, physician, origin, test_ids)
            self.order_created.emit(order, samples)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def update_result(self, result_id: int, new_value: str, user_id: int, change_reason: str = None):
        try:
            res = self.sample_service.update_result_value(result_id, new_value, user_id, change_reason)
            self.result_updated.emit(res)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def validate_result(self, result_id: int, validating_user_id: int):
        try:
            res = self.sample_service.validate_result(result_id, validating_user_id)
            self.result_validated.emit(res)
        except Exception as e:
            self.error_occurred.emit(str(e))
