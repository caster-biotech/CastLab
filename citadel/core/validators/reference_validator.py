from typing import List, Optional

from citadel.core.models.patient import Patient
from citadel.core.models.reference_range import ReferenceRange

class ReferenceValidator:
    @staticmethod
    def is_within_range(value: float, ranges: List[ReferenceRange], patient: Patient, is_pregnant: bool = False) -> Optional[bool]:
        applicable_ranges = []
        for r in ranges:
            if r.sex is not None and r.sex != patient.sex:
                continue
            if r.min_age_days is not None and patient.age_in_days < r.min_age_days:
                continue
            if r.max_age_days is not None and patient.age_in_days > r.max_age_days:
                continue
            if r.is_pregnant is not None and r.is_pregnant != is_pregnant:
                continue
            applicable_ranges.append(r)

        if not applicable_ranges:
            return None 

        for r in applicable_ranges:
            if r.min_value is not None and value < r.min_value:
                return False
            if r.max_value is not None and value > r.max_value:
                return False
        return True

    @staticmethod
    def is_qualitative_match(value: str, ranges: List[ReferenceRange], patient: Patient, is_pregnant: bool = False) -> Optional[bool]:
        applicable_ranges = []
        for r in ranges:
            if r.sex is not None and r.sex != patient.sex:
                continue
            if r.min_age_days is not None and patient.age_in_days < r.min_age_days:
                continue
            if r.max_age_days is not None and patient.age_in_days > r.max_age_days:
                continue
            if r.is_pregnant is not None and r.is_pregnant != is_pregnant:
                continue
            applicable_ranges.append(r)

        if not applicable_ranges:
            return None
            
        for r in applicable_ranges:
            if r.qualitative_text is not None and r.qualitative_text.lower() == value.lower():
                return True
        return False
