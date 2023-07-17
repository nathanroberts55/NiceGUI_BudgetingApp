from nicegui import ui
from utils import to_dict
from database.db import get_all_transactions
from constants import TRANSACTION_COLUMNS


@ui.refreshable
def transactions_tables() -> None:
    transactions = get_all_transactions()
    transactions_list = to_dict(transactions)

    ui.label("Transaction Table").classes("text-4xl my-5")
    if transactions:
        ui.table(
            columns=TRANSACTION_COLUMNS, rows=transactions_list, row_key="name"
        ).classes("mb-10")
        ui.label(
            f"Total Transaction Volume: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in transactions))}"
        ).classes("text-right")
    else:
        ui.label("No Income to Show").classes("text-semibold text-xl")
