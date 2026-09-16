from sqlmodel import Session, select
from citadel.infrastructure.database.models import OrderModel, SampleModel, ResultModel

class ReportService:
    def __init__(self, session: Session):
        self.session = session

    def get_patient_history(self, patient_id: int) -> list[dict]:
        try:
            # Query all history
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
