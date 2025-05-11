import json

from flask import Response
from pydantic import ValidationError

from loyalty.adapters.auth.idp.error import UnauthorizedError
from loyalty.adapters.exceptions.user import WebUserAlreadyExistsError
from loyalty.application.exceptions.base import (
    AccessDeniedError,
    ApplicationError,
    InvalidPaginationQueryError,
    LimitIsTooHighError,
)
from loyalty.application.exceptions.business import BusinessAlreadyExistsError, BusinessDoesNotExistError
from loyalty.application.exceptions.business_branch import (
    BusinessBranchAlreadyExistsError,
    BusinessBranchDoesNotExistError,
)
from loyalty.application.exceptions.client import ClientAlreadyExistsError, ClientDoesNotExistError
from loyalty.application.exceptions.loyalty import (
    LoyaltyAlreadyExistsError,
    LoyaltyDoesNotExistError,
    LoyaltyWrongDateTimeError,
)
from loyalty.application.exceptions.membership import MembershipAlreadyExistError, MembershipDoesNotExistError
from loyalty.application.shared_types import MAX_LIMIT

ERROR_HTTP_CODE = {
    ApplicationError: 500,
    WebUserAlreadyExistsError: 409,
    BusinessAlreadyExistsError: 409,
    BusinessBranchAlreadyExistsError: 409,
    LoyaltyAlreadyExistsError: 409,
    AccessDeniedError: 403,
    UnauthorizedError: 401,
    ClientAlreadyExistsError: 409,
    BusinessDoesNotExistError: 404,
    BusinessBranchDoesNotExistError: 404,
    LoyaltyDoesNotExistError: 404,
    LoyaltyWrongDateTimeError: 400,
    MembershipAlreadyExistError: 409,
    MembershipDoesNotExistError: 404,
    LimitIsTooHighError: 422,
    InvalidPaginationQueryError: 422,
    ClientDoesNotExistError: 404,
}

ERROR_MESSAGE = {
    ApplicationError: "Unhanded application error",
    WebUserAlreadyExistsError: "User already exists",
    BusinessAlreadyExistsError: "Business already exists",
    AccessDeniedError: "Access denied",
    UnauthorizedError: "Your aren't authorized",
    ClientAlreadyExistsError: "Client already exists",
    BusinessDoesNotExistError: "Business does not exist",
    BusinessBranchDoesNotExistError: "Business branch does not exist",
    BusinessBranchAlreadyExistsError: "Business branch already exists",
    LoyaltyDoesNotExistError: "Loyalty does not exist",
    LoyaltyAlreadyExistsError: "Loyalty already exists",
    LoyaltyWrongDateTimeError: "Loyalty start date cannot be greater than end date",
    MembershipAlreadyExistError: "Membership already exist",
    MembershipDoesNotExistError: "Membership does not exist",
    LimitIsTooHighError: f"Limit is too high (max is a {MAX_LIMIT})",
    InvalidPaginationQueryError: "Limit or offset < 0",
    ClientDoesNotExistError: "Client does not exist",
}

ERROR_CODE = {
    ApplicationError: "UNHANDLED",
    WebUserAlreadyExistsError: "USER_ALREADY_EXISTS",
    BusinessAlreadyExistsError: "BUSINESS_ALREADY_EXISTS",
    BusinessBranchAlreadyExistsError: "BUSINESS_BRANCH_ALREADY_EXISTS",
    AccessDeniedError: "ACCESS_DENIED",
    UnauthorizedError: "UNAUTHORIZED",
    ClientAlreadyExistsError: "CLIENT_ALREADY_EXISTS",
    BusinessDoesNotExistError: "BUSINESS_DOES_NOT_EXIST",
    BusinessBranchDoesNotExistError: "BUSINESS_BRANCH_DOES_NOT_EXIST",
    LoyaltyDoesNotExistError: "LOYALTY_DOES_NOT_EXIST",
    LoyaltyAlreadyExistsError: "LOYALTY_ALREADY_EXISTS",
    LoyaltyWrongDateTimeError: "LOYALTY_WRONG_DATETIME",
    MembershipAlreadyExistError: "MEMBERSHIP_ALREADY_EXIST",
    MembershipDoesNotExistError: "MEMBERSHIP_DOES_NOT_EXIST",
    LimitIsTooHighError: "LIMIT_TOO_HIGH",
    InvalidPaginationQueryError: "INVALID_PAGINATION_QUERY",
    ClientDoesNotExistError: "CLIENT_DOES_NOT_EXIST",
}

JSON_MIMETYPE = "application/json"


def validation_error_handler(e: ValidationError) -> Response:
    response = Response(e.json(), mimetype=JSON_MIMETYPE, status=422)
    return response


def app_error_handler(e: ApplicationError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }
    response = Response(json.dumps(content), mimetype=JSON_MIMETYPE, status=ERROR_HTTP_CODE[type(e)])
    return response
