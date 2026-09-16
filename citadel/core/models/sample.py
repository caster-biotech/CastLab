from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from citadel.core.models.enums import SampleStatus

@dataclass(slots=True)
class Sample:
    sample_id: int
    order_id: int
    barcode: str
    sample_type: str
    tube_type: str
    collected_at: Optional[datetime]
    status: SampleStatus
