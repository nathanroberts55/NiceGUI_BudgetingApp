from nicegui import ui
from components.budget import budget_breakdown, budget_guage
from components.category import (
    spending_breakdown_chart,
    category_treemap,
)
from components.transaction import transaction_grid, transactions_over_time_chart
from database.db import get_all_budgets
from utils import get_current_month
from components import state


def refresh_selectors() -> None:
    reporting_budget_date_select.refresh()
    viz_budget_date_select.refresh()


@ui.refreshable
def reporting_budget_date_select() -> None:
    _, first_day, last_day = get_current_month()

    with ui.row() as selection_row:
        # Budget Selection
        budget_dict = {budget.id: budget.name for budget in get_all_budgets()}
        budget_select = ui.select(
            budget_dict,
            value=(
                list(budget_dict.keys())[0] if budget_dict else "No Budgets to Select"
            ),
            label="Budget",
        ).classes("w-1/4 m-auto")
        # Start Date
        with ui.input("Start Date").classes("w-1/4 m-auto") as start_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(start_date)
            with start_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        start_date.set_value(first_day)
        # End Date
        with ui.input("End Date").classes("w-1/4 m-auto") as end_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(end_date)
            with end_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        end_date.set_value(last_day)

        (
            state.reporting_start_date,
            state.reporting_end_date,
            state.reporting_budget_id,
        ) = (start_date.value, end_date.value, budget_select.value)

        # Refresh Button
        ui.button(
            "Refresh",
            on_click=lambda: reporting_refresh(
                start_date=start_date, end_date=end_date, budget_id=budget_select
            ),
        )


def reporting_refresh(
    start_date: ui.date, end_date: ui.date, budget_id: ui.select
) -> None:
    state.reporting_start_date = start_date.value
    state.reporting_end_date = end_date.value
    state.reporting_budget_id = budget_id.value
    budget_breakdown.refresh()
    transaction_grid.refresh()


@ui.refreshable
def viz_budget_date_select() -> None:
    _, first_day, last_day = get_current_month()

    with ui.row() as selection_row:
        # Budget Selection
        budget_dict = {budget.id: budget.name for budget in get_all_budgets()}
        budget_select = ui.select(
            budget_dict,
            value=(
                list(budget_dict.keys())[0] if budget_dict else "No Budgets to Select"
            ),
            label="Budget",
        ).classes("w-1/4 m-auto")
        # Start Date
        with ui.input("Start Date").classes("w-1/4 m-auto") as start_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(start_date)
            with start_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        start_date.set_value(first_day)
        # End Date
        with ui.input("End Date").classes("w-1/4 m-auto") as end_date:
            with ui.menu() as menu:
                ui.date(mask="MM/DD/YY").bind_value(end_date)
            with end_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", menu.open).classes(
                    "cursor-pointer"
                )
        end_date.set_value(last_day)

        state.viz_start_date, state.viz_end_date, state.viz_budget_id = (
            start_date.value,
            end_date.value,
            budget_select.value,
        )

        # Refresh Button
        ui.button(
            "Refresh",
            on_click=lambda: viz_refresh(
                start_date=start_date, end_date=end_date, budget_id=budget_select
            ),
        )


def viz_refresh(start_date: ui.date, end_date: ui.date, budget_id: ui.select) -> None:
    state.viz_start_date = start_date.value
    state.viz_end_date = end_date.value
    state.viz_budget_id = budget_id.value
    transactions_over_time_chart.refresh()
    budget_guage.refresh()
    spending_breakdown_chart.refresh()
    category_treemap.refresh()
