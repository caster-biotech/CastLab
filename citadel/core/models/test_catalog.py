from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class TestCatalogItem:
    __test__ = False
    test_id: int
    code: str
    name: str
    laboratory_area: str
    unit_of_measure: str
    panic_min: Optional[float]
    panic_max: Optional[float]
