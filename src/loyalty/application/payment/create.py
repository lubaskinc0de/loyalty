import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from loyalty.application.common.gateway.bonus import BonusGateway
from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.gateway.client import ClientGateway
from loyalty.application.common.gateway.membership import MembershipGateway
from loyalty.application.common.gateway.payment import PaymentGateway
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW
from loyalty.application.exceptions.base import AccessDeniedError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.application.exceptions.client import ClientDoesNotExistError
from loyalty.application.exceptions.membership import MembershipDoesNotExistError
from loyalty.domain.common.affilation import BranchAffilationGateway
from loyalty.domain.entity.payment import Payment
from loyalty.domain.service.payment import (
    calc_bonus_income,
    calc_service_income,
    can_create_payment,
)


class PaymentForm(BaseModel):
    payment_sum: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    membership_id: UUID
    business_branch_id: UUID
    client_id: UUID
    apply_discount: bool = False


@dataclass(slots=True, frozen=True)
class PaymentCreated:
    payment_id: UUID
    payment_sum: Decimal
    service_income: Decimal
    bonus_income: Decimal
    client_id: UUID
    business_id: UUID
    bonus_spent: Decimal
    discount_sum: Decimal
    created_at: datetime


@dataclass(slots=True, frozen=True)
class CreatePayment:
    uow: UoW
    idp: BusinessIdProvider
    membership_gateway: MembershipGateway
    branch_gateway: BusinessBranchGateway
    branch_affilation_gateway: BranchAffilationGateway
    client_gateway: ClientGateway
    bonus_gateway: BonusGateway
    payment_gateway: PaymentGateway

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
        bonus_balance = self.bonus_gateway.get_bonus_balance(membership.membership_id)
        service_income = calc_service_income(form.payment_sum)
        bonus_income = calc_bonus_income(form.payment_sum, membership.loyalty.money_per_bonus, bonus_balance)
        discount_sum, bonus_spent = Decimal(0), Decimal(0)

        if form.apply_discount and bonus_balance > 0:
            new_summ, bonus_spent = membership.loyalty.apply_discount(form.payment_sum, bonus_balance)
            discount_sum = form.payment_sum - new_summ

        payment = Payment(
            payment_id=payment_id,
            payment_sum=form.payment_sum,
            service_income=service_income,
            bonus_income=bonus_income,
            client_id=client.client_id,
            business_id=membership.loyalty.business.business_id,
            loyalty_id=membership.loyalty.loyalty_id,
            membership_id=membership.membership_id,
            business_branch_id=form.business_branch_id,
            discount_sum=discount_sum,
            bonus_spent=bonus_spent,
        )

        self.uow.add(payment)
        self.uow.commit()

        payment_from_db = self.payment_gateway.get_by_id(payment.payment_id)
        if payment_from_db is None:
            logging.critical("Payment is not saved to db")
            raise AccessDeniedError

        return PaymentCreated(
            payment_id=payment_id,
            bonus_income=payment_from_db.bonus_income,
            service_income=payment_from_db.service_income,
            client_id=client.client_id,
            business_id=business.business_id,
            bonus_spent=payment_from_db.bonus_spent,
            discount_sum=payment_from_db.discount_sum,
            created_at=payment.created_at,
            payment_sum=payment_from_db.payment_sum,
        )
