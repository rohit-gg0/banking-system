from __future__ import annotations
from typing import Dict, List
from Currency import *
from Money import *
from Accounts import *
from CurrencyConverter import *
from Transaction import *

class AccountError(RuntimeError):
    pass

class Bank:

    def __init__(self):
        self._accounts : Dict[int,Account] = dict()
        self._min_balance_minor: int = 500000
        self._overdraft_limit_minor: int = 1000000
        self._next_account_id: int = 1000
        self._converter = CurrencyConverter()
        self._transactions: List[Transaction] = []
        self._transaction_attempt: List[TransactionAttempt] = []

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
        
    def withdraw(self, acc_id: int, amount: Money) -> bool:            
        if not isinstance(amount,Money):
            raise TypeError("the given amount is not vaild money")
            
        acc = self.get_account(acc_id)
            
        if amount.currency != acc.currency:
            amount = self._converter.convert(amount,acc.currency)

        try: 
            acc.withdraw(amount)
        except Exception as ex:
            ta = TransactionAttempt(TransactionType.WITHDRAW,datetime.utcnow(),amount,ex,withdraw_account=acc_id)
            self._transaction_attempt.append(ta)
            return False

        t = Transaction(TransactionType.WITHDRAW,amount,datetime.utcnow(),withdraw_acc=acc_id)
        self._transactions.append(t)
        return True
    
    def deposit(self, acc_id: int, amount: Money) -> bool:
        if not isinstance(amount,Money):
            raise TypeError("the given amount is not vaild money")
            
        acc = self.get_account(acc_id)
            
        if amount.currency != acc.currency:
            amount = self._converter.convert(amount,acc.currency)
        
        try:
            acc.deposit(amount)
        except Exception as ex:
            ta = TransactionAttempt(TransactionType.DEPOSIT,datetime.utcnow(),amount,ex,deposit_account=acc_id)
            self._transaction_attempt.append(ta)
            return False

        t = Transaction(TransactionType.DEPOSIT,amount,datetime.utcnow(),deposit_acc=acc_id)
        self._transactions.append(t)
        return True

    def transfer(self,id1: int,id2: int,amount: Money) -> bool:     
        if not isinstance(amount,Money):
            raise TypeError("the given amount is not vaild money")
            
        acc1 = self.get_account(id1)
        acc2 = self.get_account(id2)

        if acc1.currency!=amount.currency:
            amount = self._converter.convert(amount,acc1.currency)

        try:
            acc1.withdraw(amount)
        except (InsufficientFundsError, WithdrawError) as ex:
                ta = TransactionAttempt(TransactionType.TRANSFER,datetime.utcnow(),amount,ex,withdraw_account=id1,deposit_account=id2)
                self._transaction_attempt.append(ta)
                return False

        if acc2.currency!=amount.currency:
            amount = self._converter.convert(amount,acc2.currency)

        try:
            acc2.deposit(amount)
        except DepositionError as ex:
            if acc1.currency!=amount.currency:
                amount = self._converter.convert(amount,acc1.currency)
            acc1.deposit(amount)
            ta = TransactionAttempt(TransactionType.TRANSFER,datetime.utcnow(),amount,ex,withdraw_account=id1,deposit_account=id2)
            self._transaction_attempt.append(ta)
            return False

        t = Transaction(TransactionType.TRANSFER,amount,datetime.utcnow(),withdraw_acc=id1,deposit_acc=id2)
        self._transactions.append(t)
        return True
    
    @property
    def transactions(self):
        l=[]
        for t in self._transactions:
            l.append(t.__repr__())
        return l
    
    @property
    def failed_transactions(self):
        l=[]
        for t in self._transaction_attempt:
            l.append(f"{t!r}")
        return l