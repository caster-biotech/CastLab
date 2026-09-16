import pytest
from datetime import date, datetime

from citadel.core.validators.panic_validator import PanicValidator
from citadel.core.validators.reference_validator import ReferenceValidator
from citadel.core.models.test_catalog import TestCatalogItem
from citadel.core.models.reference_range import ReferenceRange
from citadel.core.models.patient import Patient
from citadel.core.models.enums import BiologicalSex

def test_panic_validator():
    test_item = TestCatalogItem(
        test_id=1, code="GLU", name="Glucose", laboratory_area="CHEMISTRY",
        unit_of_measure="mg/dL", panic_min=50.0, panic_max=400.0
    )
    
    assert PanicValidator.is_panic_value(40.0, test_item) is True
    assert PanicValidator.is_panic_value(450.0, test_item) is True
    assert PanicValidator.is_panic_value(100.0, test_item) is False

def test_reference_validator():
    patient = Patient(
        patient_id=1, national_id="123", first_name="Jane", last_name="Doe",
        birth_date=date(1990, 1, 1), sex=BiologicalSex.FEMALE, phone=None, email=None,
        created_at=datetime.now()
    )
    
    range_item = ReferenceRange(
        range_id=1, test_id=1, sex=BiologicalSex.FEMALE,
        min_age_days=None, max_age_days=None, is_pregnant=False,
        min_value=70.0, max_value=100.0, qualitative_text=None
    )
    
    assert ReferenceValidator.is_within_range(85.0, [range_item], patient, is_pregnant=False) is True
    assert ReferenceValidator.is_within_range(110.0, [range_item], patient, is_pregnant=False) is False
