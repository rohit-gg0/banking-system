from __future__ import annotations
from typing import Dict
from Money import *
from Accounts import *
from CurrencyConverter import *

class AccountError(RuntimeError):
    pass

class Bank:

    def __init__(self):
        self._accounts : Dict[int,Account] = dict()
        self._min_balance_minor: int = 500000
        self._overdraft_limit_minor: int = 1000000
        self._next_account_id: int = 1000
        self._converter = CurrencyConverter()

    def open_savings_account(self,initial_balance: Money) -> int:
        if not isinstance(initial_balance,Money):
            raise TypeError("Initial Balance is not Money")
        
        min_b = Money(self._min_balance_minor,initial_balance.currency)

        id = self._next_account_id
        account = SavingsAccount(initial_balance,min_b)
        self._accounts[id] = account

        self._next_account_id +=1

        return id

    def open_current_account(self,initial_balance: Money) -> int:
        if not isinstance(initial_balance,Money):
            raise TypeError("Initial Balance is not Money")
        
        overd = Money(self._overdraft_limit_minor,initial_balance.currency)

        id = self._next_account_id
        account = CurrentAccount(initial_balance,overd)
        self._accounts[id] = account

        self._next_account_id +=1

        return id

    def get_account(self,id: int):
        try:
            return self._accounts[id]
        except KeyError: 
            raise AccountError(f"the account with id={id} doesnot exist")
        
    def transfer(self,id1: int,id2: int,amount: Money) -> bool:     
        acc1 = self.get_account(id1)
        acc2 = self.get_account(id2)

        if acc1.currency!=amount.currency:
            amount = self._converter.convert(amount,acc1.currency)

        acc1.withdraw(amount)

        if acc2.currency!=amount.currency:
            amount = self._converter.convert(amount,acc2.currency)

        acc2.deposit(amount)

        return True    