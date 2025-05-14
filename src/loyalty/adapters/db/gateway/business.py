from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.db import business_table
from loyalty.application.business.dto import Businesses
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

    def get_businesses(self, limit: int, offset: int) -> Businesses:
        stmt = (
            select(Business)
            .limit(limit + 1)
            .offset(offset)
            .order_by(business_table.c.created_at)
        )

        result = self.session.execute(stmt)
        return Businesses(
            businesses=result.scalars().all()
        )
