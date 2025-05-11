from decimal import Decimal

SERVICE_INCOME_PERCENT = Decimal("0.05")


def calc_service_income(payment_sum: Decimal) -> Decimal:
    # посчитать прибыль сервиса с покупки
    return payment_sum * SERVICE_INCOME_PERCENT


def calc_bonus_income(payment_sum: Decimal, money_per_bonus: Decimal) -> Decimal:
    # посчитать начисление бонусов за покупку
    return payment_sum // money_per_bonus
