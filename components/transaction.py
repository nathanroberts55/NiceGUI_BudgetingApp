from nicegui import ui
from utils import to_dict
from database.db import get_all_transactions, get_budget_with_related_data
from constants import TRANSACTION_COLUMNS


def enable_next(ui_element) -> None:
    return ui_element.enable()


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


@ui.refreshable
def create_transaction_form() -> None:
    global category_select, item_name, item_budget
    budget = get_budget_with_related_data(1)

    with ui.card().classes("w-3/4 mx-auto my-10") as container:
        ui.label("Create Transaction").classes("text-semibold text-3xl")
        with ui.grid(columns=2).classes("w-full") as form:
            ui.label("Select a Category Item:").classes("text-xl m-auto")
            category_select = ui.select(
                [
                    category_item.name
                    for category in budget.categories
                    for category_item in category.category_items
                ],
                value="Select a Category",
                on_change=lambda: enable_next(transaction_date),
            ).classes("w-3/4 m-auto")

            ui.label("Transaction Date:").classes("text-xl m-auto")
            with ui.input("Income Date").classes("w-3/4 m-auto").on(
                "blur", lambda: enable_next(transaction_amount)
            ) as transaction_date:
                with ui.menu() as menu:
                    ui.date().bind_value(transaction_date)
                with transaction_date.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu.open).classes(
                        "cursor-pointer"
                    )

            transaction_date.disable()

            ui.label("Transaction Amount:").classes("text-xl m-auto")
            transaction_amount = (
                ui.number(
                    placeholder="Example: 400.00",
                    format="%.2f",
                    on_change=lambda: enable_next(save_button),
                )
                .classes("w-3/4 m-auto")
                .on(
                    "blur",
                    lambda: (transaction_amount.update(), enable_next(save_button)),
                )
            )
            transaction_amount.disable()

            ui.label()
            save_button = ui.button(
                "Save",
                on_click=lambda: (
                    save_transaction(
                        name=item_name,
                        budget=budget,
                        category_name=category_select,
                        budgeted_amount=item_budget,
                    ),
                    create_transaction_form.refresh(),
                ),
            ).classes("w-1/2 mx-auto")
            save_button.disable()
