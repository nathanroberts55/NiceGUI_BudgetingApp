from nicegui import ui
import pandas as pd
import plotly.graph_objects as go
from utils import to_dict, enable_next
from database.db import (
    get_all_transactions,
    get_transactions_by_date,
    get_all_category_items,
    get_category_item_by_id,
    update_transaction_by_id,
    delete_transaction_by_id,
    create_transaction,
)
from components import state, budget
from constants import TRANSACTION_COLUMNS, RECURRING_OPTIONS

category_item_select: ui.select = None
grid: ui.aggrid = None


def add_transaction() -> None:
    create_transaction(
        name=add_transaction_name.value,
        transaction_date=add_transaction_date.value,
        amount=f"{float(add_transaction_amount.value):.2f}",
        category_item_name=add_category_item.value,
    )

    grid.options["rowData"] = sorted(
        to_dict(
            get_transactions_by_date(
                start_date=state.reporting_start_date, end_date=state.reporting_end_date
            )
        ),
        key=lambda data: data["transaction_date"],
    )

    add_dialog.close()

    ui.notify(f"Successfully Saved {add_transaction_name.value}", color="Green")

    add_transaction_name.set_value(None)
    add_transaction_date.set_value(None)
    add_transaction_amount.set_value(None)
    add_category_item.set_value(None)

    grid.update()
    budget.budget_breakdown.refresh()


def update_transaction() -> None:
    update_transaction_by_id(
        transaction_id=state.selected_transaction["id"],
        name=edit_transaction_name.value,
        transaction_date=edit_transaction_date.value,
        amount=f"{float(edit_transaction_amount.value):.2f}",
        category_item_name=edit_category_item.value,
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

    budget.budget_breakdown.refresh()


def open_add_dialog() -> None:
    # Open the Add Transaction dialog
    add_dialog.open()


async def open_edit_dialog() -> None:
    state.selected_transaction = await grid.get_selected_row()

    if not state.selected_transaction:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    category_item = get_category_item_by_id(
        state.selected_transaction["category_item_id"]
    )

    edit_category_item.set_value(category_item.name)
    edit_transaction_name.set_value(state.selected_transaction["name"])
    edit_transaction_date.set_value(state.selected_transaction["transaction_date"])
    edit_transaction_amount.set_value(state.selected_transaction["amount"])

    edit_dialog.open()


with ui.dialog() as add_dialog:
    with ui.card():
        category_items = sorted(get_all_category_items(), key=lambda data: data.name)
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
        # region Recurring Transaction
        # add_transaction_recuring = ui.switch("Recuring Transaction").classes(
        #     "w-full  m-auto"
        # )
        # add_transaction_recurring_frequency = (
        #     ui.select(RECURRING_OPTIONS, label="Frequency", value=RECURRING_OPTIONS[0])
        #     .bind_visibility_from(add_transaction_recuring, "value")
        #     .classes("w-full m-auto")
        # )

        # # Reccuring Start Date
        # with ui.input(label="Start Date").classes("w-full m-auto").on(
        #     "blur", lambda: enable_next(add_transaction_amount)
        # ).bind_visibility_from(
        #     add_transaction_recuring, "value"
        # ) as add_recurring_start_date:
        #     with ui.menu() as menu:
        #         ui.date().bind_value(add_recurring_start_date)
        #     with add_recurring_start_date.add_slot("append"):
        #         ui.icon("edit_calendar").on("click", menu.open).classes(
        #             "cursor-pointer"
        #         )

        # # Reccuring End Date
        # with ui.input(label="End Date").classes("w-full m-auto").on(
        #     "blur", lambda: enable_next(add_transaction_amount)
        # ).bind_visibility_from(
        #     add_transaction_recuring, "value"
        # ) as add_transaction_end_date:
        #     with ui.menu() as menu:
        #         ui.date().bind_value(add_transaction_end_date)
        #     with add_transaction_end_date.add_slot("append"):
        #         ui.icon("edit_calendar").on("click", menu.open).classes(
        #             "cursor-pointer"
        #         )

        # add_transaction_recurring_dates = (
        #     ui.select(
        #         [day for day in range(1, 32)],
        #         multiple=True,
        #         value=1,
        #         label="Recurring Dates",
        #     )
        #     .bind_visibility_from(add_transaction_recuring, "value")
        #     .props("use-chips")
        #     .classes("m-auto w-full")
        # )
        # endregion Recurring Transaction
        ui.button("Save New Transaction", on_click=add_transaction).classes("m-auto")

with ui.dialog() as edit_dialog:
    with ui.card():
        category_items = sorted(get_all_category_items(), key=lambda data: data.name)
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
def transaction_grid() -> None:
    global grid
    transactions = get_transactions_by_date(
        start_date=state.reporting_start_date, end_date=state.reporting_end_date
    )
    transactions_list = to_dict(transactions)

    with ui.expansion("Transaction Table").classes("text-2xl mt-6 mb-2"):
        grid = ui.aggrid(
            {
                "defaultColDef": {"flex": 1},
                "columnDefs": [
                    {"headerName": "ID", "field": "id", "hide": True},
                    {"headerName": "ID", "field": "category_item_id", "hide": True},
                    {"headerName": "Created", "field": "created", "hide": True},
                    {"headerName": "Updated", "field": "updated", "hide": True},
                    {
                        "headerName": "Date",
                        "field": "transaction_date",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Name",
                        "field": "name",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Amount",
                        "field": "amount",
                        "valueFormatter": "'$' + value",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                ],
                "rowData": sorted(
                    transactions_list, key=lambda data: data["transaction_date"]
                ),
                "rowSelection": "single",
            }
        ).classes("max-h-120")

        with ui.row().classes("mt-4"):
            ui.button("Add", color="Green", on_click=open_add_dialog)
            ui.button("Edit", on_click=open_edit_dialog)
            ui.button("Delete", color="Red", on_click=delete_transaction)


@ui.refreshable
def transactions_over_time_chart() -> None:
    transactions = get_transactions_by_date(
        start_date=state.viz_start_date, end_date=state.viz_end_date
    )

    transactions = [
        transaction
        for transaction in transactions
        if transaction.category_item_id not in [1, 9, 10]  # Exclude Income Sources
    ]

    transaction_df = pd.DataFrame(to_dict(transactions))

    if not transaction_df.empty:
        transaction_df = transaction_df.astype(
            {
                "id": "int",
                "name": "str",
                "amount": "float",
                "transaction_date": "str",
                "created": "str",
                "updated": "str",
                "category_item_id": "int",
            }
        )

        transaction_df = transaction_df[
            [
                "id",
                "name",
                "amount",
                "transaction_date",
                "created",
                "updated",
                "category_item_id",
            ]
        ]

        transaction_df["transaction_date"] = pd.to_datetime(
            transaction_df["transaction_date"], format="%m/%d/%y"
        )
        transaction_df["created"] = pd.to_datetime(
            transaction_df["created"], format="%Y-%m-%d %H:%M:%S.%f"
        )
        transaction_df["updated"] = pd.to_datetime(
            transaction_df["updated"], format="%Y-%m-%d %H:%M:%S.%f"
        )

        grouped_transaction_df = (
            transaction_df.groupby(["transaction_date"])["amount"].sum().reset_index()
        )

        fig = go.Figure(
            data=go.Scatter(
                x=grouped_transaction_df.transaction_date,
                y=grouped_transaction_df.amount,
            )
        )

        # Set the background color to black
        fig.update_layout(
            plot_bgcolor="#1d1d1d",
            paper_bgcolor="#1d1d1d",
            font={"color": "white"},
            title=f"Spending over Period: {state.viz_start_date} - {state.viz_end_date}",
        )

        ui.plotly(fig)
    else:
        ui.label("No Data to Show for the period")
