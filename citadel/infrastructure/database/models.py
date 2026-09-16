from datetime import date, datetime
from typing import Optional
from sqlalchemy import Column, Numeric, UniqueConstraint
from sqlmodel import Field, SQLModel

from citadel.core.models.enums import (
    UserRole, BiologicalSex, OrderOrigin, OrderStatus,
    SampleStatus, ResultStatus, ResultSource
)
from citadel.core.models.user import User
from citadel.core.models.patient import Patient
from citadel.core.models.order import Order
from citadel.core.models.sample import Sample
from citadel.core.models.test_catalog import TestCatalogItem
from citadel.core.models.reference_range import ReferenceRange
from citadel.core.models.result import Result

class UserModel(SQLModel, table=True):
    __tablename__ = "users"
    
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    full_name: str
    role: UserRole
    license_number: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

    def to_domain(self) -> User:
        return User(
            user_id=self.user_id, # type: ignore
            username=self.username,
            password_hash=self.password_hash,
            full_name=self.full_name,
            role=self.role,
            license_number=self.license_number,
            is_active=self.is_active,
            created_at=self.created_at
        )

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            user_id=user.user_id,
            username=user.username,
            password_hash=user.password_hash,
            full_name=user.full_name,
            role=user.role,
            license_number=user.license_number,
            is_active=user.is_active,
            created_at=user.created_at
        )

class PatientModel(SQLModel, table=True):
    __tablename__ = "patients"
    
    patient_id: Optional[int] = Field(default=None, primary_key=True)
    national_id: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    birth_date: date
    sex: BiologicalSex
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    def to_domain(self) -> Patient:
        return Patient(
            patient_id=self.patient_id, # type: ignore
            national_id=self.national_id,
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            sex=self.sex,
            phone=self.phone,
            email=self.email,
            created_at=self.created_at
        )

    @classmethod
    def from_domain(cls, patient: Patient) -> "PatientModel":
        return cls(
            patient_id=patient.patient_id,
            national_id=patient.national_id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            birth_date=patient.birth_date,
            sex=patient.sex,
            phone=patient.phone,
            email=patient.email,
            created_at=patient.created_at
        )

class OrderModel(SQLModel, table=True):
    __tablename__ = "orders"
    
    order_id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.patient_id")
    requesting_physician: Optional[str] = None
    origin: OrderOrigin
    status: OrderStatus
    created_at: datetime = Field(default_factory=datetime.now)

    def to_domain(self) -> Order:
        return Order(
            order_id=self.order_id, # type: ignore
            patient_id=self.patient_id,
            requesting_physician=self.requesting_physician,
            origin=self.origin,
            status=self.status,
            created_at=self.created_at
        )

    @classmethod
    def from_domain(cls, order: Order) -> "OrderModel":
        return cls(
            order_id=order.order_id,
            patient_id=order.patient_id,
            requesting_physician=order.requesting_physician,
            origin=order.origin,
            status=order.status,
            created_at=order.created_at
        )

class SampleModel(SQLModel, table=True):
    __tablename__ = "samples"
    
    sample_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id")
    barcode: str = Field(unique=True, index=True)
    sample_type: str
    tube_type: str
    collected_at: Optional[datetime] = None
    status: SampleStatus

    def to_domain(self) -> Sample:
        return Sample(
            sample_id=self.sample_id, # type: ignore
            order_id=self.order_id,
            barcode=self.barcode,
            sample_type=self.sample_type,
            tube_type=self.tube_type,
            collected_at=self.collected_at,
            status=self.status
        )

    @classmethod
    def from_domain(cls, sample: Sample) -> "SampleModel":
        return cls(
            sample_id=sample.sample_id,
            order_id=sample.order_id,
            barcode=sample.barcode,
            sample_type=sample.sample_type,
            tube_type=sample.tube_type,
            collected_at=sample.collected_at,
            status=sample.status
        )

class TestCatalogModel(SQLModel, table=True):
    __tablename__ = "test_catalog"
    
    test_id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    name: str
    laboratory_area: str
    unit_of_measure: str
    panic_min: Optional[float] = Field(default=None, sa_column=Column(Numeric))
    panic_max: Optional[float] = Field(default=None, sa_column=Column(Numeric))

    def to_domain(self) -> TestCatalogItem:
        return TestCatalogItem(
            test_id=self.test_id, # type: ignore
            code=self.code,
            name=self.name,
            laboratory_area=self.laboratory_area,
            unit_of_measure=self.unit_of_measure,
            panic_min=float(self.panic_min) if self.panic_min is not None else None,
            panic_max=float(self.panic_max) if self.panic_max is not None else None
        )

    @classmethod
    def from_domain(cls, test_catalog: TestCatalogItem) -> "TestCatalogModel":
        return cls(
            test_id=test_catalog.test_id,
            code=test_catalog.code,
            name=test_catalog.name,
            laboratory_area=test_catalog.laboratory_area,
            unit_of_measure=test_catalog.unit_of_measure,
            panic_min=test_catalog.panic_min, # type: ignore
            panic_max=test_catalog.panic_max  # type: ignore
        )

class ReferenceRangeModel(SQLModel, table=True):
    __tablename__ = "reference_ranges"
    
    range_id: Optional[int] = Field(default=None, primary_key=True)
    test_id: int = Field(foreign_key="test_catalog.test_id")
    sex: Optional[BiologicalSex] = None
    min_age_days: Optional[int] = None
    max_age_days: Optional[int] = None
    is_pregnant: Optional[bool] = None
    min_value: Optional[float] = Field(default=None, sa_column=Column(Numeric))
    max_value: Optional[float] = Field(default=None, sa_column=Column(Numeric))
    qualitative_text: Optional[str] = None

    def to_domain(self) -> ReferenceRange:
        return ReferenceRange(
            range_id=self.range_id, # type: ignore
            test_id=self.test_id,
            sex=self.sex,
            min_age_days=self.min_age_days,
            max_age_days=self.max_age_days,
            is_pregnant=self.is_pregnant,
            min_value=float(self.min_value) if self.min_value is not None else None,
            max_value=float(self.max_value) if self.max_value is not None else None,
            qualitative_text=self.qualitative_text
        )

    @classmethod
    def from_domain(cls, reference_range: ReferenceRange) -> "ReferenceRangeModel":
        return cls(
            range_id=reference_range.range_id,
            test_id=reference_range.test_id,
            sex=reference_range.sex,
            min_age_days=reference_range.min_age_days,
            max_age_days=reference_range.max_age_days,
            is_pregnant=reference_range.is_pregnant,
            min_value=reference_range.min_value, # type: ignore
            max_value=reference_range.max_value, # type: ignore
            qualitative_text=reference_range.qualitative_text
        )

class ResultModel(SQLModel, table=True):
    __tablename__ = "results"
    __table_args__ = (UniqueConstraint("sample_id", "test_id"),)
    
    result_id: Optional[int] = Field(default=None, primary_key=True)
    sample_id: int = Field(foreign_key="samples.sample_id")
    test_id: int = Field(foreign_key="test_catalog.test_id")
    obtained_value: Optional[str] = None
    source: ResultSource
    analyzer_id: Optional[str] = None
    status: ResultStatus
    is_panic: bool = Field(default=False)
    evaluated_at: Optional[datetime] = None
    validated_by_user_id: Optional[int] = Field(default=None, foreign_key="users.user_id")
    validated_at: Optional[datetime] = None

    def to_domain(self) -> Result:
        return Result(
            result_id=self.result_id, # type: ignore
            sample_id=self.sample_id,
            test_id=self.test_id,
            obtained_value=self.obtained_value,
            source=self.source,
            analyzer_id=self.analyzer_id,
            status=self.status,
            is_panic=self.is_panic,
            evaluated_at=self.evaluated_at,
            validated_by_user_id=self.validated_by_user_id,
            validated_at=self.validated_at
        )

    @classmethod
    def from_domain(cls, result: Result) -> "ResultModel":
        return cls(
            result_id=result.result_id,
            sample_id=result.sample_id,
            test_id=result.test_id,
            obtained_value=result.obtained_value,
            source=result.source,
            analyzer_id=result.analyzer_id,
            status=result.status,
            is_panic=result.is_panic,
            evaluated_at=result.evaluated_at,
            validated_by_user_id=result.validated_by_user_id,
            validated_at=result.validated_at
        )

class AuditModel(SQLModel, table=True):
    __tablename__ = "result_audit_trail"
    
    audit_id: Optional[int] = Field(default=None, primary_key=True)
    result_id: int = Field(foreign_key="results.result_id")
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    change_reason: Optional[str] = None
    modified_by_user_id: int = Field(foreign_key="users.user_id")
    modified_at: datetime = Field(default_factory=datetime.now)
