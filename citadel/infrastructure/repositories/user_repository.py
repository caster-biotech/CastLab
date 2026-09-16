from typing import Optional
from sqlmodel import Session
from citadel.core.ports.repositories import UserRepository
from citadel.core.models.user import User
from citadel.infrastructure.database.models import UserModel

class SqlUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        model = self.session.get(UserModel, user_id)
        return model.to_domain() if model else None
        
    def add(self, user: User) -> User:
        model = UserModel.from_domain(user)
        self.session.add(model)
        self.session.flush()
        return model.to_domain()
