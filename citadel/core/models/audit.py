from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(slots=True)
class Audit:
    audit_id: Optional[int]
    result_id: int
    previous_value: Optional[str]
    new_value: Optional[str]
    change_reason: Optional[str]
    modified_by_user_id: int
    modified_at: datetime
