from dataclasses import dataclass
from typing import Optional

from citadel.core.models.enums import BiologicalSex

@dataclass(slots=True)
class ReferenceRange:
    range_id: int
    test_id: int
    sex: Optional[BiologicalSex]
    min_age_days: Optional[int]
    max_age_days: Optional[int]
    is_pregnant: Optional[bool]
    min_value: Optional[float]
    max_value: Optional[float]
    qualitative_text: Optional[str]
