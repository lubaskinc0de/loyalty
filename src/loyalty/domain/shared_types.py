from __future__ import annotations

from enum import Enum


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class LoyaltyTimeFrame(Enum):
    CURRENT = "CURRENT"
    UPCOMING = "UPCOMING"
    PAST = "PAST"
    ALL = "ALL"
