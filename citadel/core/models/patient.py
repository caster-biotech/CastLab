from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from citadel.core.models.enums import BiologicalSex

@dataclass(slots=True)
class Patient:
    patient_id: int
    national_id: str
    first_name: str
    last_name: str
    birth_date: date
    sex: BiologicalSex
    phone: Optional[str]
    email: Optional[str]
    created_at: datetime

    @property
    def age_in_days(self) -> int:
        return (datetime.now().date() - self.birth_date).days

    @property
    def age_in_years(self) -> int:
        today = datetime.now().date()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
