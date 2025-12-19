from enum import Enum

class Currency(Enum):
    inr = "INR"
    dlr = "DLR"
    dih = "DIH"

class CurrencyError(ValueError):
    pass

