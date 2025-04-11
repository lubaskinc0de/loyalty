from loyalty.application.exceptions.base import ApplicationError


class BusinessBranchDoesNotExistError(ApplicationError): ...


class BusinessBranchAlreadyExistsError(ApplicationError): ...
