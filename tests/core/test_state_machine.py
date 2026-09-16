import pytest
from datetime import datetime

from citadel.core.models.result import Result
from citadel.core.models.user import User
from citadel.core.models.enums import ResultStatus, ResultSource, UserRole
from citadel.core.exceptions import InvalidStateTransitionError, UnauthorizedRoleError

def test_result_validation_success():
    result = Result(
        result_id=1, sample_id=1, test_id=1, obtained_value="10.5",
        source=ResultSource.ANALYZER, analyzer_id="A1", status=ResultStatus.PENDING_VALIDATION,
        is_panic=False, evaluated_at=datetime.now(), validated_by_user_id=None, validated_at=None
    )
    user = User(
        user_id=1, username="test", password_hash="hash", full_name="Test User",
        role=UserRole.BIOANALIST, license_number="123", is_active=True, created_at=datetime.now()
    )
    
    result.transition_to(ResultStatus.VALIDATED, user)
    
    assert result.status == ResultStatus.VALIDATED
    assert result.validated_by_user_id == user.user_id
    assert result.validated_at is not None

def test_result_validation_unauthorized_role():
    result = Result(
        result_id=1, sample_id=1, test_id=1, obtained_value="10.5",
        source=ResultSource.ANALYZER, analyzer_id="A1", status=ResultStatus.PENDING_VALIDATION,
        is_panic=False, evaluated_at=datetime.now(), validated_by_user_id=None, validated_at=None
    )
    user = User(
        user_id=2, username="asst", password_hash="hash", full_name="Asst User",
        role=UserRole.ASSISTANT, license_number=None, is_active=True, created_at=datetime.now()
    )
    
    with pytest.raises(UnauthorizedRoleError):
        result.transition_to(ResultStatus.VALIDATED, user)

def test_result_invalid_transition():
    result = Result(
        result_id=1, sample_id=1, test_id=1, obtained_value="10.5",
        source=ResultSource.ANALYZER, analyzer_id="A1", status=ResultStatus.PENDING,
        is_panic=False, evaluated_at=None, validated_by_user_id=None, validated_at=None
    )
    
    with pytest.raises(InvalidStateTransitionError):
        result.transition_to(ResultStatus.VALIDATED, None)
