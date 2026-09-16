import pytest
from datetime import date, datetime
from sqlmodel import select
from citadel.application.sample_service import SampleService
from citadel.application.patient_service import PatientService
from citadel.core.models.enums import BiologicalSex, OrderOrigin, ResultStatus
from citadel.core.exceptions import UnauthorizedRoleError
from citadel.infrastructure.database.models import UserModel, AuditModel

def test_sample_service_full_lifecycle(session):
    p_service = PatientService(session)
    s_service = SampleService(session)
    
    # 1. Create Patient
    patient = p_service.register_or_get_patient({
        "national_id": "NAT-2", "first_name": "John", "last_name": "Doe",
        "birth_date": date(1980, 1, 1), "sex": BiologicalSex.MALE, "created_at": datetime.now()
    })
    
    # 2. Create Order & Sample
    order, samples = s_service.create_order_with_samples(patient.patient_id, "Dr. Smith", OrderOrigin.OUTPATIENT, [1])
    sample = samples[0]
    
    # Get Result ID created implicitly
    from citadel.infrastructure.database.models import ResultModel
    result_model = session.exec(select(ResultModel).where(ResultModel.sample_id == sample.sample_id)).first()
    result_id = result_model.result_id
    
    # 3. Enter result value (panic)
    res = s_service.update_result_value(result_id, "500", user_id=1)
    assert res.status == ResultStatus.PENDING_VALIDATION
    assert res.is_panic is True
    
    # 4. Modify existing result -> generates audit
    res_mod = s_service.update_result_value(result_id, "450", user_id=1, change_reason="Typo")
    audit = session.exec(select(AuditModel).where(AuditModel.result_id == result_id)).first()
    assert audit is not None
    assert audit.change_reason == "Typo"
    assert audit.previous_value == "500"
    assert audit.new_value == "450"
    
    # 5. Assistant tries to validate -> Error
    with pytest.raises(UnauthorizedRoleError):
        s_service.validate_result(result_id, validating_user_id=2) # User 2 is Assistant
        
    # 6. Bioanalist validates -> Success
    res_final = s_service.validate_result(result_id, validating_user_id=1) # User 1 is Bioanalist
    assert res_final.status == ResultStatus.VALIDATED
