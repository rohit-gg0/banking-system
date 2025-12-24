from enum import Enum

class Currency(Enum):
    INR = "INR"
    USD = "DLR"
    EUR = "EUR"

class CurrencyError(ValueError):
    pass

