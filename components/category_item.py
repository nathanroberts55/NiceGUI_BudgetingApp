from nicegui import ui
from database.db import (
    get_all_budgets,
    get_budget_with_related_data,
    get_budget_by_name,
    save_category_item,
    get_all_categories,
)


@ui.refreshable
def create_category_item_form() -> None:
    budget_names = ["Select a Budget"] + [budget.name for budget in get_all_budgets()]
    category_names = ["Select a Category"] + [
        category.name for category in get_all_categories()
    ]
    with ui.card().classes("w-3/4 mx-auto my-10") as container:
        ui.label("Create Budget Item").classes("text-semibold text-3xl")
        with ui.grid(columns=2).classes("w-full") as form:
            ui.label("Select a Budget:").classes("text-xl m-auto")
            budget_select = ui.select(budget_names, value=budget_names[0]).classes(
                "w-3/4 m-auto"
            )

            ui.label("Select a Category:").classes("text-xl m-auto")
            category_select = ui.select(
                category_names, value=category_names[0]
            ).classes("w-3/4 m-auto")

            ui.label("Budget Item Name:").classes("text-xl m-auto")
            budget_select = ui.input(
                placeholder="Example: Rent, Paycheck, etc."
            ).classes("w-3/4 m-auto")

            ui.label()
            ui.button(
                "Save",
                on_click=lambda: (
                    save_category_item(),
                    create_category_item_form.refresh(),
                ),
            ).classes("w-1/2 mx-auto")
