from sqlmodel import Session
from citadel.core.ports.repositories import AuditRepository
from citadel.infrastructure.database.models import AuditModel

class SqlAuditRepository(AuditRepository):
    def __init__(self, session: Session):
        self.session = session

    def log_action(self, action: str, details: str) -> None:
        pass
