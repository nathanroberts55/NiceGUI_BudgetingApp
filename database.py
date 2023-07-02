import pandas as pd
from nicegui import ui
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import List

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


def get_transactions(ledger):
    income_transactions = [transaction for transaction in ledger.transactions if transaction.trans_type == TransactionType.INCOME]
    expense_transactions = [transaction for transaction in ledger.transactions if transaction.trans_type == TransactionType.EXPENSE]
    return [income_transactions, expense_transactions]

# Data Visualization
def get_transaction_data(ledger: Ledger) -> pd.DataFrame:
    budget_data = pd.DataFrame([vars(t) for t in ledger.transactions])
    budget_data['trans_type'] = budget_data['trans_type'].apply(lambda x: 'Income' if x == TransactionType.INCOME else 'Expense')
    grouped_data = budget_data.groupby('trans_type')['amount'].sum().reset_index()

    return grouped_data

def save_income(ledger, income_date, income_source, income_amount) -> None:
    date = datetime.strptime(income_date.value, '%Y-%m-%d')
    ledger.save(
        date.strftime('%m/%d/%y'),
        TransactionType.INCOME,
        income_source.value,
        float("{:.2f}".format(income_amount.value))
    )

    ui.notify(f'{income_source.value} Saved!')


def save_expense(ledger,expense_date, expense_source, expense_amount) -> None:
    date = datetime.strptime(expense_date.value, '%Y-%m-%d')
    ledger.save(
        date.strftime('%m/%d/%y'),
        TransactionType.EXPENSE,
        expense_source.value,
        float("{:.2f}".format(expense_amount.value))
    )

    ui.notify(f'{expense_source.value} Saved!')

