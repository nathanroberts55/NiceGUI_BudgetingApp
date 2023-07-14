from nicegui import ui

# from database.db import get_transactions
from constants import INCOME_TABLE_COLUMNS, EXPENSE_TABLE_COLUMNS


@ui.refreshable
def transactions_tables() -> None:
    # income_transactions, expense_transactions = get_transactions()
    # Income Table
    ui.label("Income Table").classes("text-4xl my-5")
    # if income_transactions:
    #     ui.table(
    #         columns=INCOME_TABLE_COLUMNS, rows=income_transactions, row_key="name"
    #     ).classes("mb-10")
    #     ui.label(
    #         f"Total Income: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in income_transactions))}"
    #     ).classes("text-right")
    # else:
    #     ui.label("No Income to Show").classes("text-semibold text-xl")

    # Expense Table
    ui.markdown("Expense Table").classes("text-4xl my-5")
    # if expense_transactions:
    #     ui.table(
    #         columns=EXPENSE_TABLE_COLUMNS, rows=expense_transactions, row_key="name"
    #     ).classes("mb-10")
    #     ui.label(
    #         f"Total Expenses: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in expense_transactions))}"
    #     ).classes("text-right")
    # else:
    #     ui.label("No Expenses to Show").classes("text-semibold text-xl")
