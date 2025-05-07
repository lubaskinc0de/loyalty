from loyalty.application.exceptions.base import ApplicationError


class MembershipDoesNotExistError(ApplicationError): ...


class MembershipAlreadyExistError(ApplicationError): ...
