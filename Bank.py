from __future__ import annotations
from datetime import datetime
from typing import Dict, List
from Money import Money
from Accounts import Account,SavingsAccount,CurrentAccount,InsufficientFundsError,WithdrawError,DepositionError
from CurrencyConverter import CurrencyConverter
from Transaction import Transaction,TransactionAttempt,TransactionType

class AccountError(RuntimeError):
    pass

class WrongPassword(ValueError):
    pass

class Bank:

    def __init__(self):
        self._accounts : Dict[int,Account] = dict()
        self._acc_passwords: Dict[int,str] = dict()
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
        print("Enter a password")
        while True:
            password = input("(alphanumeric only)>>>").strip()
            if password.isalnum():
                break

        account = SavingsAccount(initial_balance,min_b)
        self._accounts[id] = account
        self._acc_passwords[id] = password

        self._next_account_id +=10

        return id

    def open_current_account(self,initial_balance: Money) -> int:
        if not isinstance(initial_balance,Money):
            raise TypeError("Initial Balance is not Money")
        
        overd = Money(self._overdraft_limit_minor,initial_balance.currency)

        id = self._next_account_id
        print("Enter a password")
        while True:
            password = input("(alphanumeric only)>>>").strip()
            if password.isalnum():
                break

        account = CurrentAccount(initial_balance,overd)
        self._accounts[id] = account
        self._acc_passwords[id] = password

        self._next_account_id +=1

        return id

    def get_account(self,id: int):
        
        c=0
        while True:
            try:
                if id not in self._accounts:
                    raise KeyError()
                print("Enter the password")
                password = input(">>>").strip()
                if self._acc_passwords[id]!=password:
                    c=c+1
                    raise ValueError("Wrong Password")
                return self._accounts[id]
            except ValueError as v:
                print("Wrong Password")
                if c>=3:
                    print("3 wrong attempts, program terminating")
                    raise WrongPassword("Wrong Password")
            except KeyError: 
                raise AccountError(f"the account with id={id} doesnot exist")
        
    def check_balance(self,acc_id: int) -> Money:
        acc = self.get_account(acc_id)
        return acc.balance
        
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
    def transactions(self) -> List[str]:
        l=[]
        for t in self._transactions:
            l.append(t.__repr__())
        return l
    
    @property
    def failed_transactions(self) -> List[str]:
        l=[]
        for t in self._transaction_attempt:
            l.append(f"{t!r}")
        return l
    
    @property
    def get_min_balance_savings_minor(self) -> int:
        return self._min_balance_minor
    
    @property
    def get_overdraft_limit_minor(self) -> int:
        return self._overdraft_limit_minor
    
    def get_acc_transaction_history(self,id: int) -> List[str]:
        l=[]
        self.get_account(id)

        for t in self._transactions:
            if t._deposit_acc == id or t._withdraw_acc == id:
                l.append(f"{t!r}")

        for t in self._transaction_attempt:
            if t.withdraw_account == id or t.deposit_account == id:
                l.append(f"{t!r}")

        return l