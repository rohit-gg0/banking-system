from __future__ import annotations
from Money import *
from Currency import *

class CurrencyConverter:
    dlr_rates = {
        Currency.dlr:1,
        Currency.inr:81,
        Currency.dih:69
        }

    def convert(self,money: Money,to: Currency) -> Money:
        if not isinstance(money,Money):
            raise TypeError("the given money is not money")

        if not isinstance(to,Currency):
            raise ValueError("the given currecny does not exist")
        
        amt = money.amount*self.dlr_rates[money.currency]
        amt = amt/self.dlr_rates[to]

        return Money(amt,to)