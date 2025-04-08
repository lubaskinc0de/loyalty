from loyalty.application.exceptions.base import ApplicationError


class BusinessAlreadyExistsError(ApplicationError): ...


class BusinessDoesNotExistsError(ApplicationError): ...
