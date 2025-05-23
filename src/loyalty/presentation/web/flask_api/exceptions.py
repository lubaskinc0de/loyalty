from loyalty.application.exceptions.base import ApplicationError


class MissingImageError(ApplicationError): ...


class EmptyFilenameError(ApplicationError): ...


class IsNotImageError(ApplicationError): ...


class MissingFileExtensionError(ApplicationError): ...
