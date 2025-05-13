from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.payment import PaymentGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.payment import PaymentDoesNotExistError
from loyalty.domain.entity.payment import Payment


@dataclass(slots=True, frozen=True)
class ReadPayment:
    idp: BusinessIdProvider
    gateway: PaymentGateway

    def execute(self, payment_id: UUID) -> Payment:
        business = self.idp.get_business()
        payment = self.gateway.get_by_id(payment_id)

        if payment is None:
            raise PaymentDoesNotExistError

        if not payment.can_read(business):
            raise AccessDeniedError

        return payment
