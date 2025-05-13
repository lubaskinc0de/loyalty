from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from loyalty.application.common.gateway.payment import PaymentGateway
from loyalty.domain.entity.payment import Payment


@dataclass(slots=True, frozen=True)
class SAPaymentGateway(PaymentGateway):
    session: Session

    def get_by_id(self, payment_id: UUID) -> Payment | None:
        q = select(Payment).filter_by(payment_id=payment_id)
        res = self.session.execute(q).scalar_one_or_none()
        return res
