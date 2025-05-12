from pydantic_extra_types.phone_numbers import PhoneNumber

MAX_LIMIT = 100
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0


class RussianPhoneNumber(PhoneNumber):
    supported_regions = ["ru"]  # noqa: RUF012
