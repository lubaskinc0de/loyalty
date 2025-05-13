from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from loyalty.adapters.db import payment_table
from loyalty.application.common.gateway.bonus import BonusGateway


@dataclass(slots=True, frozen=True)
class SABonusGateway(BonusGateway):
    session: Session

    def get_bonus_balance(self, membership_id: UUID) -> Decimal:
        q = (
            select(
                func.sum(payment_table.c.bonus_income),
            )
            .select_from(payment_table)
            .where(
                payment_table.c.membership_id == membership_id,
            )
            .group_by(payment_table.c.membership_id)
        )

        res = self.session.execute(q).scalar_one_or_none()
        return Decimal(res) if res is not None else Decimal("0.0")
