from typing import Optional

from citadel.core.models.test_catalog import TestCatalogItem

class PanicValidator:
    @staticmethod
    def is_panic_value(value: float, test_item: TestCatalogItem) -> bool:
        if test_item.panic_min is not None and value < test_item.panic_min:
            return True
        if test_item.panic_max is not None and value > test_item.panic_max:
            return True
        return False
