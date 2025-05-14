from dataclasses import dataclass
from uuid import UUID

from loyalty.application.common.gateway.payment import PaymentGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.payment import PaymentDoesNotExistError


@dataclass(slots=True, frozen=True)
class DeletePayment:
    idp: BusinessIdProvider
    gateway: PaymentGateway
    uow: UoW

    def execute(self, payment_id: UUID) -> None:
        business = self.idp.get_business()
        payment = self.gateway.get_by_id(payment_id)

        if payment is None:
            raise PaymentDoesNotExistError

        if not payment.can_delete(business):
            raise AccessDeniedError

        self.uow.delete(payment)
        self.uow.commit()
