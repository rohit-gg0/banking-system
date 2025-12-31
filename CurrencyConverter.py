from __future__ import annotations
from typing import Dict
from Money import Money
from Currency import Currency

class CurrencyConverter:
    dlr_rates: Dict[Currency,int] = {
        Currency.USD:1,
        Currency.INR:81,
        Currency.EUR:25,
        }

    def convert(self,money: Money,to: Currency) -> Money:
        if not isinstance(money,Money):
            raise TypeError("the given money is not money")

        if not isinstance(to,Currency):
            raise ValueError("the given currecny does not exist")
        
        amt = money.amount/self.dlr_rates[money.currency]
        amt = int(round(amt*self.dlr_rates[to]))

        return Money(amt,to)