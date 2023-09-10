import plotly.graph_objects as go
from nicegui import ui
from utils import to_dict
import components
from database.db import (
    get_all_budgets,
    get_budget_data_by_date,
    initialize_budget,
    get_budget_by_id,
    update_budget_by_id,
    delete_budget_by_id,
)


grid: ui.aggrid = None
delete_budget_name: str = None


def placeholder_func() -> None:
    ui.notify(f"Running Placeholder function")


def add_budget() -> None:
    initialize_budget(
        name=add_budget_name.value,
    )

    grid.options["rowData"] = sorted(
        to_dict(get_all_budgets()),
        key=lambda data: data["name"],
    )

    add_dialog.close()

    ui.notify(f"Successfully Saved {add_budget_name.value}", color="Green")

    add_budget_name.set_value(None)

    grid.update()
    components.common.refresh_selectors()


def update_budget() -> None:
    update_budget_by_id(
        budget_id=components.state.selected_budget["id"],
        name=edit_budget_name.value,
    )

    grid.options["rowData"] = sorted(
        to_dict(get_all_budgets()),
        key=lambda data: data["name"],
    )

    ui.notify(f"Successfully Updated {edit_budget_name.value}")

    edit_dialog.close()
    grid.update()
    components.common.refresh_selectors()


async def delete_budget() -> None:
    row = await grid.get_selected_row()

    if not row:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    delete_budget_by_id(row["id"])

    grid.options["rowData"] = sorted(
        to_dict(get_all_budgets()),
        key=lambda data: data["name"],
    )

    grid.update()

    ui.notify(f"Successfully Deleted {row['name']}", color="Red")

    delete_dialog.close()
    components.common.refresh_selectors()


with ui.dialog() as add_dialog:
    with ui.card():
        # Budget Name
        add_budget_name = ui.input(
            label="Budget Name",
        ).classes("w-full m-auto")

        ui.button("Save Budget", on_click=add_budget).classes("m-auto")

with ui.dialog() as edit_dialog:
    with ui.card():
        # Budget Name
        edit_budget_name = ui.input(
            label="Budget Name",
        ).classes("w-full m-auto")

        ui.button("Edit Budget", on_click=update_budget).classes("m-auto")

with ui.dialog() as delete_dialog:
    with ui.card():
        delete_budget_label = ui.label(
            f"Confirm that you want to delete {delete_budget_name}"
        )

        with ui.row().classes("m-auto"):
            ui.button("Confirm", color="green", on_click=delete_budget).classes(
                "m-auto"
            )
            ui.button("Cancel", color="red", on_click=delete_dialog.close).classes(
                "m-auto"
            )


def open_add_dialog() -> None:
    # Open the Add Transaction dialog
    add_dialog.open()


async def open_edit_dialog() -> None:
    components.state.selected_budget = await grid.get_selected_row()

    if not components.state.selected_budget:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    budget = get_budget_by_id(components.state.selected_budget["id"])

    edit_budget_name.set_value(budget.name)

    edit_dialog.open()


async def open_delete_dialog() -> None:
    components.state.selected_budget = await grid.get_selected_row()

    if not components.state.selected_budget:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    budget = get_budget_by_id(components.state.selected_budget["id"])

    delete_budget_label.set_text(f"Confirm that you want to delete {budget.name}")

    delete_dialog.open()


@ui.refreshable
def budget_grid() -> None:
    global grid
    budgets = get_all_budgets()
    budgets_list = to_dict(budgets)

    ui.label("Budget Table").classes("text-semibold text-3xl my-5")

    grid = ui.aggrid(
        {
            "defaultColDef": {"flex": 1},
            "columnDefs": [
                {"headerName": "ID", "field": "id", "hide": True},
                {"headerName": "Created", "field": "created", "hide": True},
                {"headerName": "Updated", "field": "updated", "hide": True},
                {
                    "headerName": "Name",
                    "field": "name",
                    "filter": "agTextColumnFilter",
                    "floatingFilter": True,
                },
            ],
            "rowData": sorted(budgets_list, key=lambda data: data["name"]),
            "rowSelection": "single",
        }
    ).classes("max-h-92")

    with ui.row().classes("mt-4"):
        ui.button("Add", color="Green", on_click=open_add_dialog)
        ui.button("Edit", on_click=open_edit_dialog)
        ui.button("Delete", color="Red", on_click=open_delete_dialog)


@ui.refreshable
def budget_breakdown() -> None:
    if not get_all_budgets():
        ui.label("No Budget to Breakdown")
    else:
        budget = get_budget_data_by_date(
            budget_id=components.state.reporting_budget_id,
            start_date=components.state.reporting_start_date,
            end_date=components.state.reporting_end_date,
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
                ui.label("$ {:.2f}".format(category.budgeted_total)).classes(
                    "text-bold"
                )
                ui.label("$ {:.2f}".format(category.actual_total)).classes("text-bold")
                ui.label("{:.2f}%".format(category.percent_of_budget)).classes(
                    "text-bold"
                )
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
            ui.label(f"$ {'{:.2f}'.format(budget.budgeted_balance)}").classes(
                "text-bold"
            )
            ui.label(f"$ {'{:.2f}'.format(budget.actual_balance)}").classes("text-bold")
        ui.splitter(horizontal=True)


@ui.refreshable
def budget_guage() -> None:
    if not get_all_budgets():
        ui.label("No Budget Data")
    else:
        budget = get_budget_data_by_date(
            budget_id=components.state.viz_budget_id,
            start_date=components.state.viz_start_date,
            end_date=components.state.viz_end_date,
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
