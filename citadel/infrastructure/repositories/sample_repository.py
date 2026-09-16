from typing import Optional
from sqlmodel import Session
from citadel.core.ports.repositories import SampleRepository
from citadel.core.models.sample import Sample
from citadel.infrastructure.database.models import SampleModel

class SqlSampleRepository(SampleRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, sample_id: int) -> Optional[Sample]:
        model = self.session.get(SampleModel, sample_id)
        return model.to_domain() if model else None

    def add(self, sample: Sample) -> Sample:
        model = SampleModel.from_domain(sample)
        self.session.add(model)
        self.session.flush()
        return model.to_domain()
