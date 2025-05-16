from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.adapters.db.table.loyalty import loyalty_table
from loyalty.application.common.gateway.loyalty import LoyaltyGateway
from loyalty.application.exceptions.loyalty import LoyaltyAlreadyExistsError
from loyalty.application.loyalty.dto import Loyalties, convert_loyalties_to_dto
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import Gender, LoyaltyTimeFrame


@dataclass(slots=True, frozen=True)
class SALoyaltyGateway(LoyaltyGateway):
    session: Session

    def get_by_id(self, loyalty_id: UUID) -> Loyalty | None:
        return self.session.get(Loyalty, loyalty_id)

    def get_loyalties(
        self,
        limit: int,
        offset: int,
        business_id: UUID | None,
        time_frame: LoyaltyTimeFrame,
        active: bool | None = True,
        client_age: int | None = None,
        client_gender: Gender | None = None,
    ) -> Loyalties:
        stmt = select(Loyalty).limit(limit).offset(offset).order_by(loyalty_table.c.created_at)

        if active is not None:
            stmt = stmt.where(loyalty_table.c.is_active == active)
        if client_gender:
            stmt = stmt.where((loyalty_table.c.gender == client_gender) | (loyalty_table.c.gender.is_(None)))
        if client_age:
            stmt = stmt.where((loyalty_table.c.min_age <= client_age) & (client_age <= loyalty_table.c.max_age))
        if business_id:
            stmt = stmt.where(loyalty_table.c.business_id == business_id)

        if time_frame == LoyaltyTimeFrame.CURRENT:
            stmt = stmt.where(
                (loyalty_table.c.starts_at <= datetime.now(tz=UTC)) & (datetime.now(tz=UTC) <= loyalty_table.c.ends_at),
            )

        res = self.session.execute(stmt)
        return Loyalties(
            business_id=business_id,
            loyalties=convert_loyalties_to_dto(res.scalars().all()),
        )

    def try_insert_unique(self, loyalty: Loyalty) -> None:
        try:
            self.session.add(loyalty)
            self.session.flush((loyalty,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "uq_loyalty_name":
                    raise LoyaltyAlreadyExistsError from e
                case _:
                    raise

    def try_ensure_unique(self, loyalty: Loyalty) -> None:
        try:
            self.session.flush((loyalty,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "uq_loyalty_name":
                    raise LoyaltyAlreadyExistsError from e
                case _:
                    raise
