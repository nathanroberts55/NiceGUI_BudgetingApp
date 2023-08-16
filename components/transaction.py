from nicegui import ui
from utils import to_dict, enable_next
from database.db import (
    get_all_transactions,
    get_budget_with_related_data,
    get_transactions_by_date,
    get_all_category_items,
    get_category_item_by_id,
    update_transaction_by_id,
    get_transaction_by_id,
    delete_transaction_by_id,
    save_transaction,
)
from components import state, budget
from constants import TRANSACTION_COLUMNS, RECURRING_OPTIONS

category_item_select: ui.select = None
grid: ui.aggrid = None


def add_transaction() -> None:
    # TODO: Create Transaction Here

    add_dialog.close()

    ui.notify("Successfully Saved Transaction", color="Green")


def update_transaction() -> None:
    # TODO: Update Transaction Here
    update_transaction_by_id(
        transaction_id=state.selected_row["id"],
        name=edit_transaction_name.value,
        transaction_date=edit_transaction_date.value,
        amount=f"{float(edit_transaction_amount.value)}",
        category_item_id=state.selected_row["category_item_id"],
    )

    grid.options["rowData"] = sorted(
        to_dict(
            get_transactions_by_date(
                start_date=state.reporting_start_date, end_date=state.reporting_end_date
            )
        ),
        key=lambda data: data["transaction_date"],
    )

    ui.notify(f"Successfully Updated {edit_transaction_name.value}")

    edit_dialog.close()
    grid.update()
    budget.budget_breakdown.refresh()


async def delete_transaction() -> None:
    row = await grid.get_selected_row()

    if not row:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    delete_transaction_by_id(row["id"])

    grid.options["rowData"] = sorted(
        to_dict(
            get_transactions_by_date(
                start_date=state.reporting_start_date, end_date=state.reporting_end_date
            )
        ),
        key=lambda data: data["transaction_date"],
    )

    grid.update()

    ui.notify("Successfully Deleted Transaction", color="Red")


def open_add_dialog() -> None:
    # Open the Add Transaction dialog
    add_dialog.open()


async def open_edit_dialog() -> None:
    state.selected_row = await grid.get_selected_row()

    if not state.selected_row:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    category_item = get_category_item_by_id(state.selected_row["category_item_id"])

    edit_category_item.set_value(category_item.name)
    edit_transaction_name.set_value(state.selected_row["name"])
    edit_transaction_date.set_value(state.selected_row["transaction_date"])
    edit_transaction_amount.set_value(state.selected_row["amount"])

    edit_dialog.open()


with ui.dialog() as add_dialog:
    with ui.card():
        category_items = get_all_category_items()
        add_category_item = ui.select(
            [category_item.name for category_item in category_items],
            value="Select a Category",
        ).classes("w-full")
        add_transaction_name = ui.input(
            placeholder="Example: Taco Bell",
        ).classes("w-full")
        with ui.input("Transaction Date").classes(
            "w-full m-auto"
        ) as add_transaction_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(add_transaction_date)
            with add_transaction_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        add_transaction_amount = (
            ui.number(
                placeholder="Example: 400.00",
                format="%.2f",
            )
            .classes("w-full m-auto")
            .on(
                "blur",
                lambda: add_transaction_amount.update(),
            )
        )
        ui.button("Save New Transaction", on_click=add_transaction).classes("m-auto")

with ui.dialog() as edit_dialog:
    with ui.card():
        category_items = get_all_category_items()
        edit_category_item = ui.select(
            [category_item.name for category_item in category_items],
        ).classes("w-full")
        edit_transaction_name = ui.input().classes("w-full")
        with ui.input("Transaction Date").classes(
            "w-full m-auto"
        ) as edit_transaction_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(edit_transaction_date)
            with edit_transaction_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        edit_transaction_amount = (
            ui.number(
                format="%.2f",
            )
            .classes("w-full m-auto")
            .on(
                "blur",
                lambda: edit_transaction_amount.update(),
            )
        )
        ui.button("Edit Transaction", on_click=update_transaction).classes("m-auto")


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


@ui.refreshable
def transaction_grid() -> None:
    global grid
    transactions = get_transactions_by_date(
        start_date=state.reporting_start_date, end_date=state.reporting_end_date
    )
    transactions_list = to_dict(transactions)

    ui.label("Transaction Table").classes("text-2xl mt-6 mb-2")
    grid = ui.aggrid(
        {
            "defaultColDef": {"flex": 1},
            "columnDefs": [
                {"headerName": "ID", "field": "id", "hide": True},
                {"headerName": "ID", "field": "category_item_id", "hide": True},
                {"headerName": "Created", "field": "created", "hide": True},
                {"headerName": "Updated", "field": "updated", "hide": True},
                {"headerName": "Date", "field": "transaction_date"},
                {"headerName": "Name", "field": "name"},
                {
                    "headerName": "Amount",
                    "field": "amount",
                    "valueFormatter": "'$' + value",
                },
            ],
            "rowData": sorted(
                transactions_list, key=lambda data: data["transaction_date"]
            ),
            "rowSelection": "single",
        }
    ).classes("max-h-80")

    with ui.row().classes("mt-4"):
        ui.button("Add", color="Green", on_click=open_add_dialog)
        ui.button("Edit", on_click=open_edit_dialog)
        ui.button("Delete", color="Red", on_click=delete_transaction)
