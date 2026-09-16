from typing import Optional
from sqlmodel import Session
from citadel.core.ports.repositories import ResultRepository
from citadel.core.models.result import Result
from citadel.infrastructure.database.models import ResultModel

class SqlResultRepository(ResultRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, result_id: int) -> Optional[Result]:
        model = self.session.get(ResultModel, result_id)
        return model.to_domain() if model else None

    def add(self, result: Result) -> Result:
        model = ResultModel.from_domain(result)
        self.session.add(model)
        self.session.flush()
        return model.to_domain()
