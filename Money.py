from __future__ import annotations
from Currency import *

class Money:
    def __init__(self,amount: int, currency: Currency):
        if isinstance(amount,bool) or  not isinstance(amount,int):
            raise TypeError("Amount must be int (minor units)")
        
        if not isinstance(currency,Currency):
            raise TypeError(f"Invalid Currency {currency}")

        self._amount = amount        
        self._currency = currency

    @property
    def amount(self):
        return self._amount
    
    @property
    def currency(self):
        return self._currency
    
    def _assetr_compatible(self,other: Money) -> None:
        if not isinstance(other,Money):
            raise TypeError(f"the give object is not Money")
        if self._currency!=other._currency:
            raise CurrencyError(f"The currencies do not match")

    def add(self, other: Money) -> Money:
        self._assetr_compatible(other)
        return Money(self._amount+other._amount,self._currency)
    
    def subtract(self, other: Money) -> Money:
        self._assetr_compatible(other)
        return Money(self._amount-other._amount,self._currency)
    
    def __eq__(self, other: Money) -> bool:
        if not isinstance(other,Money):
            return False
        return (self._currency == other._currency) and (self._amount == other._amount)
    
    def __lt__(self, other: Money) -> bool:
        if not isinstance(other,Money):
            return NotImplemented
        
        if self._currency!=other._currency:
            raise CurrencyError(f"The currencies doesnot match")
        
        return self._amount<other._amount
    
    def __le__(self, other: Money) -> bool:
        if not isinstance(other,Money):
            return NotImplemented
        
        if self._currency!=other._currency:
            raise CurrencyError(f"The currencies doesnot match")
        
        return self._amount<=other._amount
    
    def __gt__(self, other: Money) -> bool:
        if not isinstance(other,Money):
            return NotImplemented
        
        if self._currency!=other._currency:
            raise CurrencyError(f"The currencies doesnot match")
        
        return self._amount>other._amount
    
    def __ge__(self, other: Money) -> bool:
        if not isinstance(other,Money):
            return NotImplemented
        
        if self._currency!=other._currency:
            raise CurrencyError(f"The currencies doesnot match")
        
        return self._amount>=other._amount
    
    def __repr__(self) -> str:
        return f"Money(amount={self._amount}, currency={self._currency})"
    
    def __str__(self) -> str:
        return f"{self._amount/100:.2f} {self._currency.value!r}"
    
    def __hash__(self):
        return hash((self._amount,self._currency))
    