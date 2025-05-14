from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy.sql import functions

from loyalty.adapters.db import business_table, client_table, payment_table
from loyalty.application.common.gateway.statistic import StatisticsGateway


@dataclass(slots=True, frozen=True)
class SAStatisticsGateway(StatisticsGateway):
    session: Session

    def get_total_payments(self) -> Decimal:
        stmt = functions.sum(payment_table.c.payment_sum)
        result = self.session.execute(stmt).scalar_one_or_none()

        return Decimal(result) if result is not None else Decimal("0.0")

    def get_total_clients(self) -> int:
        stmt = functions.count(client_table.c.client_id)
        result = self.session.execute(stmt).scalar_one_or_none()

        return result if result is not None else 0

    def get_total_businesses(self) -> int:
        stmt = functions.count(business_table.c.business_id)
        result = self.session.execute(stmt).scalar_one_or_none()

        return result if result is not None else 0
