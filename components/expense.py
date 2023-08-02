from nicegui import ui
from database.db import save_expense
from constants import RECURRING_OPTIONS


@ui.refreshable
def expense_entry() -> None:
    with ui.column().classes("w-1/2"):
        ui.label("Expense Entry").classes("text-semibold text-3xl my-5")
        with ui.input("Expense Date") as expense_date:
            with ui.menu() as menu:
                ui.date().bind_value(expense_date)
            with expense_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        expense_source = ui.input(
            label="Expense Source",
        )
        expense_amount = ui.number(label="Expense Amount", value=0.00, format="%.2f")
        expense_recuring = ui.switch("Recuring Expense")
        expense_recurring_frequency = (
            ui.select(RECURRING_OPTIONS, label="Frequency", value=RECURRING_OPTIONS[0])
            .bind_visibility_from(expense_recuring, "value")
            .classes("ml-10 w-36")
        )
        expense_recurring_dates = (
            ui.select(
                [day for day in range(1, 32)], multiple=True, value=1, label="Day"
            )
            .bind_visibility_from(expense_recuring, "value")
            .props("use-chips")
            .classes("ml-10 w-36")
        )
        ui.button(
            text="Submit",
            on_click=lambda: (
                save_expense(expense_date, expense_source, expense_amount),
                expense_entry.refresh(),
            ),
        )
