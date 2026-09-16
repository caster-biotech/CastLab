from sqlmodel import Session
from citadel.core.ports.repositories import AuditRepository
from citadel.infrastructure.database.models import AuditModel
from citadel.core.models.audit import Audit

class SqlAuditRepository(AuditRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, audit: Audit) -> Audit:
        model = AuditModel.from_domain(audit)
        self.session.add(model)
        self.session.flush()
        return model.to_domain()
