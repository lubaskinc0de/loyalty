from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.gateway.client import ClientGateway
from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.application.exceptions.client import ClientDoesNotExistError
from loyalty.application.exceptions.membership import MembershipDoesNotExistError
from loyalty.domain.entity.payment import Payment
from loyalty.domain.service.payment import (
    BranchAffilationGateway,
    calc_bonus_income,
    calc_service_income,
    can_create_payment,
)


class PaymentForm(BaseModel):
    payment_sum: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    membership_id: UUID
    business_branch_id: UUID
    client_id: UUID


@dataclass(slots=True, frozen=True)
class PaymentCreated:
    payment_id: UUID
    service_income: Decimal
    bonus_income: Decimal
    client_id: UUID
    business_id: UUID


@dataclass(slots=True, frozen=True)
class CreatePayment:
    uow: UoW
    idp: BusinessIdProvider
    membership_gateway: MembershipGateway
    branch_gateway: BusinessBranchGateway
    branch_affilation_gateway: BranchAffilationGateway
    client_gateway: ClientGateway

    def execute(self, form: PaymentForm) -> PaymentCreated:
        business = self.idp.get_business()
        membership = self.membership_gateway.get_by_id(form.membership_id)
        client = self.client_gateway.get_by_id(form.client_id)
        business_branch = self.branch_gateway.get_by_id(form.business_branch_id)

        if membership is None:
            raise MembershipDoesNotExistError

        if client is None:
            raise ClientDoesNotExistError

        if business_branch is None:
            raise BusinessBranchDoesNotExistError

        if not can_create_payment(membership, client, business, business_branch, self.branch_affilation_gateway):
            raise AccessDeniedError

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

        return PaymentCreated(
            payment_id=payment_id,
            bonus_income=bonus_income,
            service_income=service_income,
            client_id=client.client_id,
            business_id=business.business_id,
        )
