from __future__ import annotations
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from Currency import *
from Money import *
from enum import Enum

class TransactionType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    TRANSFER = 'transfer'

class Transaction:
    def __init__(self,transaction_type: TransactionType, amount: Money,
                 timestamp: Optional[datetime]=None,
                 withdraw_acc: Optional[int]=None,
                 deposit_acc: Optional[int]=None
                 ):
        if not isinstance(transaction_type,TransactionType):
            raise TypeError("the given transaction type DNE")
        if not isinstance(amount,Money):
            raise TypeError("the given amount is not money")
        
        self._transaction_type = transaction_type
        self._amount = amount
        self._withdraw_acc = withdraw_acc
        self._deposit_acc = deposit_acc
        self._timestamp = timestamp or datetime.utcnow()

    def __repr__(self):
        if self._transaction_type == TransactionType.DEPOSIT:
            return (
                f"Transaction Type: {self._transaction_type}\n"
                f"Amount: {self._amount!r}\n"
                f"Account id: {self._deposit_acc}\n"
                f"Timestamp: {self._timestamp!r}\n"
            )
        if self._transaction_type == TransactionType.WITHDRAW:
            return (
                f"Transaction Type: {self._transaction_type}\n"
                f"Amount: {self._amount!r}\n"
                f"Account id: {self._withdraw_acc}\n"
                f"Timestamp: {self._timestamp!r}\n"
            )
        
        return (
            f"Transaction Type: {self._transaction_type}\n"
            f"Amount: {self._amount!r}\n"
            f"Withdraw Account id: {self._withdraw_acc}\n"
            f"Deposit Account id: {self._deposit_acc}\n"
            f"Timestamp: {self._timestamp!r}\n"
        )

@dataclass
class TransactionAttempt:
    transaction_type: TransactionType
    timestamp: datetime
    amount: Money
    error: Exception
    withdraw_account: Optional[int] = None
    deposit_account: Optional[int] = None

    def __repr__(self):
        if self.transaction_type == TransactionType.DEPOSIT:
            return (
                f"[FAILED {self.transaction_type.value.upper()}]\n"
                f"Amount: {self.amount!r}\n"
                f"Account id: {self.deposit_acc}\n"
                f"Timestamp: {self.timestamp!r}\n"
                f"Error: {type(self.error).__name__}: {self.error}\n"
            )
        if self.transaction_type == TransactionType.WITHDRAW:
            return (
                f"[FAILED {self.transaction_type.value.upper()}]\n"
                f"Amount: {self.amount!r}\n"
                f"Account id: {self.withdraw_acc}\n"
                f"Timestamp: {self.timestamp!r}\n"
                f"Error: {type(self.error).__name__}: {self.error}\n"
            )
            
        return (
            f"[FAILED {self.transaction_type.value.upper()}]\n"
            f"Amount: {self.amount!r}\n"
            f"Withdraw Account id: {self.withdraw_acc}\n"
            f"Deposit Account id: {self.deposit_acc}\n"
            f"Timestamp: {self.timestamp!r}\n"
            f"Error: {type(self.error).__name__}: {self.error}\n"
        )