import plotly.graph_objects as go
from nicegui import ui
from utils import get_current_month
from components import state
from database.db import get_all_budgets, get_budget_data_by_date, save_budget


@ui.refreshable
def create_budget_form() -> None:
    with ui.card().classes("w-3/4 mx-auto") as container:
        ui.label("Create New Budget").classes("text-semibold text-3xl")
        with ui.grid(columns=2).classes("w-full") as form:
            ui.label("Enter a Budget Name:").classes("text-xl m-auto")
            name = ui.input(label="Budget Name").classes("w-3/4 m-auto")

            ui.label()
            ui.button(
                "Save",
                on_click=lambda: (save_budget(name), create_budget_form.refresh()),
            ).classes("w-1/2 mx-auto")


@ui.refreshable
def budget_breakdown() -> None:
    budget = get_budget_data_by_date(
        1, start_date=state.reporting_start_date, end_date=state.reporting_end_date
    )
    ui.label(budget.name).classes("text-semibold text-3xl my-5")
    with ui.grid(columns=5):
        ui.label("Name").classes("text-semibold ml-20")
        ui.label("Budget")
        ui.label("Acutal")
        ui.label("% of Budgeted Income")
        ui.label("Over\\Under")
    ui.splitter(horizontal=True)
    for category in budget.categories:
        ui.label(category.name).classes("text-semibold text-2xl ml-10")
        for category_item in category.category_items:
            with ui.grid(columns=5):
                ui.label(category_item.name).classes("text-semibold ml-20")
                ui.label("$ {:.2f}".format(float(category_item.budgeted)))
                ui.label("$ {:.2f}".format(category_item.actual))
                ui.label("{:.2f}%".format(category_item.percent_of_budget))
                ui.label(
                    (
                        lambda x: "($ {:.2f})".format(abs(x))
                        if x < 0
                        else "$ {:.2f}".format(x)
                    )(category_item.over_under)
                )
        with ui.grid(columns=5):
            ui.label("TOTAL").classes("text-bold ml-20")
            ui.label("$ {:.2f}".format(category.budgeted_total)).classes("text-bold")
            ui.label("$ {:.2f}".format(category.actual_total)).classes("text-bold")
            ui.label("{:.2f}%".format(category.percent_of_budget)).classes("text-bold")
            ui.label(
                (
                    lambda x: "($ {:.2f})".format(abs(x))
                    if x < 0
                    else "$ {:.2f}".format(x)
                )(category.over_under)
            ).classes("text-bold")
        ui.splitter(horizontal=True)
    ui.splitter(horizontal=True).classes("mt-2")
    with ui.grid(columns=5):
        ui.label("Budget Total Balance").classes("text-bold ml-20")
        ui.label(f"$ {'{:.2f}'.format(budget.budgeted_balance)}").classes("text-bold")
        ui.label(f"$ {'{:.2f}'.format(budget.actual_balance)}").classes("text-bold")
    ui.splitter(horizontal=True)


@ui.refreshable
def budget_guage() -> None:
    budget = get_budget_data_by_date(
        1, start_date=state.reporting_start_date, end_date=state.reporting_end_date
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=budget.actual_total_out,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Total Spending vs Total Income"},
            delta={"reference": budget.actual_total_in},
            gauge={
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": budget.actual_total_in,
                },
            },
        )
    )

    # Set the background color to black
    fig.update_layout(
        plot_bgcolor="#1d1d1d", paper_bgcolor="#1d1d1d", font={"color": "white"}
    )

    ui.plotly(fig)
