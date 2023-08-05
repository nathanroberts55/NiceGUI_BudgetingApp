from nicegui import ui
from components.budget import budget_breakdown
from components.category import transactions_tables_by_category
from utils import get_current_month
from components import state


def budget_date_select() -> None:
    _, first_day, last_day = get_current_month()

    with ui.row() as selection_row:
        # Start Date
        ui.label("Start Date:").classes("text-xl m-auto")
        with ui.input("Transaction Date").classes("w-1/4 m-auto") as start_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(start_date)
            with start_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        start_date.set_value(first_day)
        # End Date
        ui.label("End Date:").classes("text-xl m-auto")
        with ui.input("Transaction Date").classes("w-1/4 m-auto") as end_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(end_date)
            with end_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        end_date.set_value(last_day)

        state.reporting_start_date, state.reporting_end_date = (
            start_date.value,
            end_date.value,
        )

        # Refresh Button
        ui.button(
            "Refresh",
            on_click=lambda: date_select_onclick(
                start_date=start_date, end_date=end_date
            ),
        )


def date_select_onclick(start_date: ui.date, end_date: ui.date) -> None:
    state.reporting_start_date = start_date.value
    state.reporting_end_date = end_date.value
    budget_breakdown.refresh()
    transactions_tables_by_category.refresh()