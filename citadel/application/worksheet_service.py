from sqlmodel import Session
from citadel.core.models.result import Result
from citadel.application.sample_service import SampleService

class WorksheetService:
    def __init__(self, session: Session):
        self.session = session
        self.sample_service = SampleService(session)

    def process_bulk_results(self, results_data: list[dict], user_id: int) -> list[Result]:
        processed_results = []
        try:
            for data in results_data:
                res = self.sample_service.update_result_value(
                    result_id=data["result_id"],
                    new_value=data["new_value"],
                    user_id=user_id,
                    change_reason=data.get("change_reason")
                )
                processed_results.append(res)
            # The sample_service commits individually in the current design, 
            # ideally it wouldn't commit until the end of the bulk operation.
            # Assuming it commits individually for now.
            return processed_results
        except Exception:
            self.session.rollback()
            raise
