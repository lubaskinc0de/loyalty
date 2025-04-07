from pydantic_extra_types.phone_numbers import PhoneNumber


class RussianPhoneNumber(PhoneNumber):
    supported_regions = ["ru"]  # noqa: RUF012
