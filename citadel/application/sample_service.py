from sqlmodel import Session, select
from datetime import datetime
import uuid
from citadel.core.models.enums import OrderOrigin, OrderStatus, SampleStatus, ResultStatus, ResultSource
from citadel.core.models.order import Order
from citadel.core.models.sample import Sample
from citadel.core.models.result import Result
from citadel.infrastructure.database.models import TestCatalogModel, UserModel, ResultModel
from citadel.infrastructure.repositories.order_repository import SqlOrderRepository
from citadel.infrastructure.repositories.sample_repository import SqlSampleRepository
from citadel.infrastructure.repositories.result_repository import SqlResultRepository
from citadel.infrastructure.repositories.audit_repository import SqlAuditRepository
from citadel.core.validators.panic_validator import PanicValidator
from citadel.core.validators.reference_validator import ReferenceValidator

class SampleService:
    def __init__(self, session: Session):
        self.session = session
        self.order_repo = SqlOrderRepository(session)
        self.sample_repo = SqlSampleRepository(session)
        self.result_repo = SqlResultRepository(session)
        self.audit_repo = SqlAuditRepository(session)

    def create_order_with_samples(self, patient_id: int, physician: str, origin: OrderOrigin, test_ids: list[int]) -> tuple[Order, list[Sample]]:
        try:
            order = Order(
                order_id=None, # type: ignore
                patient_id=patient_id,
                requesting_physician=physician,
                origin=origin,
                status=OrderStatus.REGISTERED,
                created_at=datetime.now()
            )
            saved_order = self.order_repo.add(order)
            
            sample = Sample(
                sample_id=None, # type: ignore
                order_id=saved_order.order_id,
                barcode=f"BC-{uuid.uuid4().hex[:8].upper()}",
                sample_type="BLOOD",
                tube_type="EDTA",
                collected_at=None,
                status=SampleStatus.PENDING
            )
            saved_sample = self.sample_repo.add(sample)
            
            for test_id in test_ids:
                result = Result(
                    result_id=None, # type: ignore
                    sample_id=saved_sample.sample_id,
                    test_id=test_id,
                    obtained_value=None,
                    source=ResultSource.MANUAL,
                    analyzer_id=None,
                    status=ResultStatus.PENDING,
                    is_panic=False,
                    evaluated_at=None,
                    validated_by_user_id=None,
                    validated_at=None
                )
                self.result_repo.add(result)
                
            self.session.commit()
            return saved_order, [saved_sample]
        except Exception:
            self.session.rollback()
            raise

    def update_result_value(self, result_id: int, new_value: str, user_id: int, change_reason: str | None = None) -> Result:
        try:
            result = self.result_repo.get_by_id(result_id)
            if not result:
                raise ValueError("Result not found")
                
            if result.status != ResultStatus.PENDING and not change_reason:
                raise ValueError("change_reason is required when modifying a non-pending result")
                
            if result.obtained_value is not None or result.status != ResultStatus.PENDING:
                from citadel.core.models.audit import Audit
                audit = Audit(
                    audit_id=None,
                    result_id=result.result_id,
                    previous_value=result.obtained_value,
                    new_value=new_value,
                    change_reason=change_reason or "Update",
                    modified_by_user_id=user_id,
                    modified_at=datetime.now()
                )
                self.audit_repo.add(audit)
            
            result.obtained_value = new_value
            result.status = ResultStatus.PENDING_VALIDATION
            result.evaluated_at = datetime.now()
            
            test_model = self.session.get(TestCatalogModel, result.test_id)
            if test_model:
                try:
                    num_val = float(new_value)
                    result.is_panic = PanicValidator.is_panic_value(num_val, test_model.to_domain())
                except ValueError:
                    pass 
            
            result_model = self.session.get(ResultModel, result_id)
            result_model.obtained_value = result.obtained_value
            result_model.status = result.status
            result_model.evaluated_at = result.evaluated_at
            result_model.is_panic = result.is_panic
            self.session.add(result_model)
            self.session.commit()
            
            return result
        except Exception:
            self.session.rollback()
            raise

    def validate_result(self, result_id: int, validating_user_id: int) -> Result:
        try:
            user_model = self.session.get(UserModel, validating_user_id)
            if not user_model:
                raise ValueError("User not found")
                
            result = self.result_repo.get_by_id(result_id)
            if not result:
                raise ValueError("Result not found")
                
            result.transition_to(ResultStatus.VALIDATED, user_model.to_domain())
            
            result_model = self.session.get(ResultModel, result_id)
            result_model.status = result.status
            result_model.validated_by_user_id = result.validated_by_user_id
            result_model.validated_at = result.validated_at
            self.session.add(result_model)
            
            self.session.commit()
            return result
        except Exception:
            self.session.rollback()
            raise
