from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.db import business_table, loyalty_membership_table, loyalty_table, payment_table
from loyalty.application.business.dto import BusinessPaymentsStats
from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.exceptions.business import BusinessAlreadyExistsError
from loyalty.domain.entity.business import Business


@dataclass(slots=True, frozen=True)
class SABusinessGateway(BusinessGateway):
    session: Session

    def try_insert_unique(self, business: Business) -> None:
        try:
            self.session.add(business)
            self.session.flush((business,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "business_name_key":
                    raise BusinessAlreadyExistsError from e
                case _:
                    raise

    def get_by_id(self, business_id: UUID) -> Business | None:
        q = select(Business).filter_by(business_id=business_id)
        res = self.session.execute(q).scalar_one_or_none()
        return res

    def get_businesses(self, limit: int, offset: int) -> Sequence[Business]:
        stmt = select(Business).limit(limit).offset(offset).order_by(business_table.c.created_at)

        result = self.session.execute(stmt)
        return result.scalars().all()

    def get_business_payments_stat(self, business_id: UUID) -> BusinessPaymentsStats:
        q = (
            select(
                func.sum(payment_table.c.payment_sum),
                func.sum(payment_table.c.bonus_income),
                func.sum(payment_table.c.service_income),
            )
            .select_from(payment_table)
            .where(
                payment_table.c.business_id == business_id,
            )
            .group_by(payment_table.c.business_id)
        )

        res = self.session.execute(q).first()
        if res is None:
            return BusinessPaymentsStats(
                payments_amount=Decimal(0),
                waste_amount=Decimal(0),
                bonus_given_amount=Decimal(0),
            )

        payment_amount, bonus_amount, service_income = res
        return BusinessPaymentsStats(
            payments_amount=payment_amount,
            waste_amount=service_income,
            bonus_given_amount=bonus_amount,
        )

    def get_business_loyalties_count(self, business_id: UUID) -> int:
        q = (
            select(func.count(loyalty_table.c.loyalty_id))
            .select_from(loyalty_table)
            .where(
                loyalty_table.c.business_id == business_id,
            )
        )
        res = self.session.execute(q).scalar_one_or_none()
        return res or 0

    def get_business_memberships_count(self, business_id: UUID) -> int:
        q = (
            select(func.count(loyalty_membership_table.c.membership_id))
            .join(loyalty_table, loyalty_table.c.loyalty_id == loyalty_membership_table.c.loyalty_id)
            .select_from(loyalty_membership_table)
            .where(
                loyalty_table.c.business_id == business_id,
            )
        )
        res = self.session.execute(q).scalar_one_or_none()
        return res or 0
