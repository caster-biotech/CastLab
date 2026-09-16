from typing import Optional
from sqlmodel import Session
from citadel.core.ports.repositories import OrderRepository
from citadel.core.models.order import Order
from citadel.infrastructure.database.models import OrderModel

class SqlOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: int) -> Optional[Order]:
        model = self.session.get(OrderModel, order_id)
        return model.to_domain() if model else None

    def add(self, order: Order) -> Order:
        model = OrderModel.from_domain(order)
        self.session.add(model)
        self.session.flush()
        return model.to_domain()
