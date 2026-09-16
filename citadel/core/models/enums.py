from enum import StrEnum, auto

class UserRole(StrEnum):
    BIOANALIST = auto()
    ASSISTANT = auto()
    MASTER = auto()

class BiologicalSex(StrEnum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()

class OrderOrigin(StrEnum):
    EMERGENCY = auto()
    HOSPITALIZATION = auto()
    OUTPATIENT = auto()

class OrderStatus(StrEnum):
    REGISTERED = auto()
    IN_PROCESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()

class SampleStatus(StrEnum):
    PENDING = auto()
    COLLECTED = auto()
    RECEIVED = auto()
    REJECTED = auto()

class ResultStatus(StrEnum):
    PENDING = auto()
    IN_PROCESSING = auto()
    PENDING_VALIDATION = auto()
    VALIDATED = auto()
    CORRECTED = auto()

class ResultSource(StrEnum):
    MANUAL = auto()
    ANALYZER = auto()
