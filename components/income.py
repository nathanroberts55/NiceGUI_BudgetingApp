from nicegui import ui
from database.db import save_income


@ui.refreshable
def income_entry() -> None:
    # income_transactions, _ = get_transactions()
    # Income Entry
    # income_autocomplete_options = [
    #     transaction.source for transaction in income_transactions
    # ]
    with ui.column().classes("w-1/2"):
        ui.label("Income Entry").classes("text-semibold text-3xl my-5")
        with ui.input("Income Date") as income_date:
            with ui.menu() as menu:
                ui.date().bind_value(income_date)
            with income_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        income_source = ui.input(
            label="Income Source",
        )
        income_amount = ui.number(label="Income Amount", value=0.00, format="%.2f")
        ui.button(
            text="Submit",
            on_click=lambda: (
                save_income(income_date, income_source, income_amount),
                income_entry.refresh(),
            ),
        )
