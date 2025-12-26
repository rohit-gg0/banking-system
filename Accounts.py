from __future__ import annotations
import abc
from Money import Money
from Currency import Currency,CurrencyError

class InsufficientFundsError(RuntimeError):
    pass

class WithdrawError(RuntimeError):
    pass

class DepositionError(RuntimeError):
    pass

class Account(abc.ABC):
    def __init__(self,initial_balance: Money, min_balance: Money) -> None:
        if not isinstance(initial_balance,Money):
            raise TypeError(f"Initial_Balance is not Money")
        if not isinstance(min_balance,Money):
            raise TypeError(f"Initial_Balance is not Money")
        
        if initial_balance.currency!=min_balance.currency:
            raise CurrencyError("Initial_balance and min_balance not the same currency")
        
        if initial_balance.amount < min_balance.amount:
            raise ValueError("Initial Balance cannot be less than the minimum Balance")
        
        self._balance = initial_balance
        self._min_balance = min_balance

    def _assert_can_withdraw(self, amount: Money) -> None:
        if (self._balance.subtract(amount)) < self._min_balance:
            raise InsufficientFundsError("Insufficient Funds")
        
        if amount.amount <=0:
            raise WithdrawError("cant withdraw 0 or negative")

    def withdraw(self, amount: Money) -> None:
        if not isinstance(amount,Money):
            raise TypeError(f"the given amount is not Money")
        
        if self._balance.currency!=amount.currency:
            raise CurrencyError("Inavlid currency for this account")
        
        self._assert_can_withdraw(amount)
                
        self._balance = self._balance.subtract(amount)

    def deposit(self, amount: Money) -> None:
        if not isinstance(amount,Money):
            raise TypeError(f"the given amount is not Money")
        
        if self._balance.currency!=amount.currency:
            raise CurrencyError("Inavlid currency for this account")
        
        if amount.amount <= 0:
            raise DepositionError("Cant deposit 0 or negative amount")
        
        self._balance = self._balance.add(amount)

    @property
    def balance(self) -> Money:
        return self._balance
    
    @property
    def currency(self) -> Currency:
        return self._balance.currency
    
class SavingsAccount(Account):
    pass

class CurrentAccount(Account):
    def __init__(self, initial_balance: Money, overdraft_limit: Money):

        if not isinstance(overdraft_limit,Money):
            raise TypeError(f"Initial_Balance is not Money")
        
        if overdraft_limit.amount <=0:
            raise ValueError("Overdraft limint cant be 0 or negtive")
        
        if initial_balance.currency!=overdraft_limit.currency:
            raise CurrencyError("overdraft limit and initial babance are not the same currency")
        
        min_balance = Money(-overdraft_limit.amount,overdraft_limit.currency)
        super().__init__(initial_balance,min_balance)