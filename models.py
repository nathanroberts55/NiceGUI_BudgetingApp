from dataclasses import dataclass, field
from enum import Enum
from typing import List
from components import transactions_tables

class TransactionType(Enum):
    INCOME: int = 1
    EXPENSE: int = 2

@dataclass
class Transaction:
    date: str
    trans_type: TransactionType
    source: str
    amount: float
    is_recurring: bool = False
    recurring_schedule: str = ''
    recurring_date: str = ''
    _next_id: int = 0
    id: int = field(init=False)

    def __post_init__(self):
        self.id = Transaction._next_id
        Transaction._next_id += 1

@dataclass
class Ledger:
    on_change: List[callable]
    transactions: List[Transaction] = field(default_factory=list)

    def save(self, date: str, trans_type: TransactionType, source: str, amount: float) -> None:
        self.transactions.append(Transaction(date, trans_type, source, amount))
        for func in self.on_change:
            func()

ledger = Ledger([transactions_tables.refresh])
