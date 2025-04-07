from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from loyalty.application.common.gateway.business_gateway import BusinessGateway
from loyalty.application.exceptions.business import BusinessAlreadyExistsError
from loyalty.domain.entity.business import Business


@dataclass(slots=True, frozen=True)
class SABusinessGateway(BusinessGateway):
    session: Session

    def insert(self, business: Business) -> None:
        try:
            self.session.add(business)
            self.session.flush((business,))
        except IntegrityError as e:
            match e.orig.diag.constraint_name:  # type: ignore
                case "uq_business_name":
                    raise BusinessAlreadyExistsError from e
                case _:
                    raise
