from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import ClientIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.membership import MembershipDoesNotExistError
from loyalty.domain.entity.payment import Payment
from loyalty.domain.service.payment import calc_bonus_income, calc_service_income


class PaymentForm(BaseModel):
    payment_sum: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    membership_id: UUID


@dataclass(slots=True, frozen=True)
class CreatePayment:
    uow: UoW
    idp: ClientIdProvider
    membership_gateway: MembershipGateway

    def execute(self, form: PaymentForm) -> UUID:
        client = self.idp.get_client()
        membership = self.membership_gateway.get_by_id(form.membership_id)

        if membership is None:
            raise MembershipDoesNotExistError

        payment_id = uuid4()
        service_income = calc_service_income(form.payment_sum)
        bonus_income = calc_bonus_income(form.payment_sum, membership.loyalty.money_per_bonus)
        payment = Payment(
            payment_id=payment_id,
            payment_sum=form.payment_sum,
            service_income=service_income,
            bonus_income=bonus_income,
            client_id=client.client_id,
            business_id=membership.loyalty.business.business_id,
            loyalty_id=membership.loyalty.loyalty_id,
            membership_id=membership.membership_id,
        )

        self.uow.add(payment)
        self.uow.commit()

        return payment_id
