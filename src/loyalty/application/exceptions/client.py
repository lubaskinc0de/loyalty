from loyalty.application.exceptions.base import ApplicationError


class ClientAlreadyExistsError(ApplicationError): ...


class ClientDoesNotExistError(ApplicationError): ...
