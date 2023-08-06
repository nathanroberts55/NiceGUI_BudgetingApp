from nicegui import ui
from utils import to_dict, enable_next
from database.db import (
    get_all_transactions,
    get_budget_with_related_data,
    save_transaction,
)
from constants import TRANSACTION_COLUMNS, RECURRING_OPTIONS

category_item_select: ui.select = None


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
    global category_select
    budget = get_budget_with_related_data(1)

    with ui.card().classes("w-3/4 mx-auto my-10") as container:
        ui.label("Create Transaction").classes("text-semibold text-3xl")
        with ui.grid(columns=2).classes("w-full") as form:
            ui.label("Select a Category Item:").classes("text-xl m-auto")
            category_item_select = ui.select(
                [
                    category_item.name
                    for category in budget.categories
                    for category_item in category.category_items
                ],
                value="Select a Category",
                on_change=lambda: enable_next(transaction_name),
            ).classes("w-3/4 m-auto")

            ui.label("Transaction Name:").classes("text-xl m-auto")
            transaction_name = ui.input(
                placeholder="Example: Taco Bell",
                on_change=lambda: enable_next(transaction_date),
            ).classes("w-3/4 m-auto")
            transaction_name.disable()

            # Transaction Date
            ui.label("Transaction Date:").classes("text-xl m-auto")
            with ui.input("Transaction Date").classes("w-3/4 m-auto").on(
                "blur", lambda: enable_next(transaction_amount)
            ) as transaction_date:
                with ui.menu() as menu:
                    ui.date(mask="MM/DD/YY").bind_value(transaction_date)
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

            # region Recurring Transaction
            # transaction_recuring = ui.switch("Recuring Transaction").classes(
            #     "w-3/4 text-xl m-auto"
            # )
            # transaction_recurring_frequency = (
            #     ui.select(
            #         RECURRING_OPTIONS, label="Frequency", value=RECURRING_OPTIONS[0]
            #     )
            #     .bind_visibility_from(transaction_recuring, "value")
            #     .classes("w-3/4 m-auto")
            # )

            # # Reccuring Start Date
            # ui.label("Start Date:").classes("text-xl m-auto").bind_visibility_from(
            #     transaction_recuring, "value"
            # )
            # with ui.input("Start Date").classes("w-3/4 m-auto").on(
            #     "blur", lambda: enable_next(transaction_amount)
            # ).bind_visibility_from(
            #     transaction_recuring, "value"
            # ) as recurring_start_date:
            #     with ui.menu() as menu:
            #         ui.date().bind_value(recurring_start_date)
            #     with recurring_start_date.add_slot("append"):
            #         ui.icon("edit_calendar").on("click", menu.open).classes(
            #             "cursor-pointer"
            #         )

            # # Reccuring End Date
            # ui.label("End Date:").classes("text-xl m-auto").bind_visibility_from(
            #     transaction_recuring, "value"
            # )
            # with ui.input("End Date").classes("w-3/4 m-auto").on(
            #     "blur", lambda: enable_next(transaction_amount)
            # ).bind_visibility_from(transaction_recuring, "value") as transaction_date:
            #     with ui.menu() as menu:
            #         ui.date().bind_value(transaction_date)
            #     with transaction_date.add_slot("append"):
            #         ui.icon("edit_calendar").on("click", menu.open).classes(
            #             "cursor-pointer"
            #         )

            # ui.label("Recurring Dates").bind_visibility_from(
            #     transaction_recuring, "value"
            # ).classes("text-xl m-auto")
            # transaction_recurring_dates = (
            #     ui.select(
            #         [day for day in range(1, 32)], multiple=True, value=1, label="Day"
            #     )
            #     .bind_visibility_from(transaction_recuring, "value")
            #     .props("use-chips")
            #     .classes("m-auto w-3/4")
            # )
            # endregion Recurring Transaction

            ui.label()
            save_button = ui.button(
                "Save",
                on_click=lambda: (
                    save_transaction(
                        name=transaction_name,
                        transaction_date=transaction_date,
                        category_item_name=category_item_select,
                        amount=transaction_amount,
                    ),
                    create_transaction_form.refresh(),
                ),
            ).classes("w-1/2 mx-auto")
            save_button.disable()
