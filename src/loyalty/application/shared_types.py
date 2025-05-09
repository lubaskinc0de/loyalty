from pydantic_extra_types.phone_numbers import PhoneNumber

MAX_LIMIT = 100


class RussianPhoneNumber(PhoneNumber):
    supported_regions = ["ru"]  # noqa: RUF012
