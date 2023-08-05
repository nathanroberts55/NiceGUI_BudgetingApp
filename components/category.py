from nicegui import ui
from utils import to_dict
from components import state
from database.db import get_category_data_by_date, get_all_categories
from constants import TRANSACTION_COLUMNS


def category_list() -> None:
    categories = get_all_categories()
    for category in categories:
        ui.label(category.name)


@ui.refreshable
def transactions_tables_by_category() -> None:
    category_ids = [category.id for category in get_all_categories()]

    for id in category_ids:
        category = get_category_data_by_date(
            category_id=id,
            start_date=state.reporting_start_date,
            end_date=state.reporting_end_date,
        )
        transactions = [
            transaction
            for category_item in category.category_items
            for transaction in category_item.transactions
        ]
        if transactions:
            transactions_list = to_dict(transactions)
            ui.label(f"{category.name} Transactions").classes("text-4xl my-5")
            ui.table(
                columns=TRANSACTION_COLUMNS, rows=transactions_list, row_key="name"
            ).classes("mb-10")
            ui.label(
                f"Total Transaction Volume: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in transactions))}"
            ).classes("text-right")
        else:
            ui.label(f"No {category.name} to Show").classes("text-semibold text-xl")
