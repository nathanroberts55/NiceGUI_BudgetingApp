from nicegui import ui
from database.db import get_all_budgets, get_budget_with_related_data, save_budget


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


def budget_breakdown() -> None:
    budget = get_budget_with_related_data(1)
    ui.label(budget.name).classes("text-semibold text-3xl my-5")
    ui.splitter(horizontal=True)
    for category in budget.categories:
        ui.label(category.name).classes("text-semibold text-2xl ml-10")
        for category_item in category.category_items:
            with ui.grid(columns=3):
                ui.label(category_item.name).classes("text-semibold ml-20")
                ui.label("{:.2f}".format(float(category_item.budgeted)))
                ui.label("{:.2f}".format(category_item.actual))
        with ui.grid(columns=3):
            ui.label("TOTAL").classes("text-bold ml-20")
            ui.label("{:.2f}".format(category.budgeted_total)).classes("text-bold")
            ui.label("{:.2f}".format(category.actual_total)).classes("text-bold")
        ui.splitter(horizontal=True)
    ui.splitter(horizontal=True).classes("mt-2")
    with ui.grid(columns=3):
        ui.label("Budget Total Balance").classes("text-bold ml-20")
        ui.label(f"$ {'{:.2f}'.format(budget.budgeted_balance)}").classes("text-bold")
        ui.label(f"$ {'{:.2f}'.format(budget.actual_balance)}").classes("text-bold")
    ui.splitter(horizontal=True)
