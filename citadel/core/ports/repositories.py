from abc import ABC, abstractmethod
from typing import Optional

from citadel.core.models.user import User
from citadel.core.models.patient import Patient
from citadel.core.models.order import Order
from citadel.core.models.sample import Sample
from citadel.core.models.result import Result

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

class PatientRepository(ABC):
    @abstractmethod
    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

class SampleRepository(ABC):
    @abstractmethod
    def get_by_id(self, sample_id: int) -> Optional[Sample]:
        pass

class ResultRepository(ABC):
    @abstractmethod
    def get_by_id(self, result_id: int) -> Optional[Result]:
        pass

from citadel.core.models.audit import Audit

class AuditRepository(ABC):
    @abstractmethod
    def add(self, audit: Audit) -> Audit:
        pass
