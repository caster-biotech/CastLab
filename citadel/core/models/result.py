from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from citadel.core.exceptions import InvalidStateTransitionError, UnauthorizedRoleError
from citadel.core.models.enums import ResultStatus, ResultSource, UserRole
from citadel.core.models.user import User

@dataclass(slots=True)
class Result:
    result_id: int
    sample_id: int
    test_id: int
    obtained_value: Optional[str]
    source: ResultSource
    analyzer_id: Optional[str]
    status: ResultStatus
    is_panic: bool
    evaluated_at: Optional[datetime]
    validated_by_user_id: Optional[int]
    validated_at: Optional[datetime]

    def transition_to(self, new_status: ResultStatus, user: Optional[User] = None) -> None:
        if new_status == ResultStatus.VALIDATED:
            self._validate(user)
            self.validated_by_user_id = user.user_id if user else None
            self.validated_at = datetime.now()
        elif new_status == ResultStatus.PENDING_VALIDATION:
            if self.status not in (ResultStatus.PENDING, ResultStatus.IN_PROCESSING):
                raise InvalidStateTransitionError(f"Cannot transition from {self.status} to {new_status}")
        elif new_status == ResultStatus.IN_PROCESSING:
            if self.status != ResultStatus.PENDING:
                raise InvalidStateTransitionError(f"Cannot transition from {self.status} to {new_status}")
        
        self.status = new_status
        
    def _validate(self, user: Optional[User]) -> None:
        if self.status != ResultStatus.PENDING_VALIDATION:
            raise InvalidStateTransitionError(f"Result must be in PENDING_VALIDATION to be validated, current: {self.status}")
        if not user:
            raise UnauthorizedRoleError("User must be provided for validation")
        if user.role != UserRole.BIOANALIST:
            raise UnauthorizedRoleError("Only a BIOANALIST can validate results")
