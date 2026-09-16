from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from citadel.core.models.enums import OrderOrigin, OrderStatus

@dataclass(slots=True)
class Order:
    order_id: int
    patient_id: int
    requesting_physician: Optional[str]
    origin: OrderOrigin
    status: OrderStatus
    created_at: datetime
