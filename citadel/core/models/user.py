from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from citadel.core.models.enums import UserRole

@dataclass(slots=True)
class User:
    user_id: int
    username: str
    password_hash: str
    full_name: str
    role: UserRole
    license_number: Optional[str]
    is_active: bool
    created_at: datetime
