from nicegui import ui
from database.db import (
    get_budget_with_related_data,
    save_category_item,
)


category_select: ui.select = None
item_name: ui.input = None
item_budget: ui.number = None
save_button: ui.button = None
budget = None


def enable_next(ui_element) -> None:
    return ui_element.enable()


@ui.refreshable
def create_category_item_form() -> None:
    global category_select, item_name, item_budget
    budget = get_budget_with_related_data(1)

    with ui.card().classes("w-3/4 mx-auto my-10") as container:
        ui.label("Create Budget Item").classes("text-semibold text-3xl")
        with ui.grid(columns=2).classes("w-full") as form:
            # Category Select
            ui.label("Select a Category:").classes("text-xl m-auto")
            category_select = ui.select(
                [category.name for category in budget.categories],
                value="Select a Category",
                on_change=lambda: enable_next(item_name),
            ).classes("w-3/4 m-auto")
            # Category Item Name
            ui.label("Budget Item Name:").classes("text-xl m-auto")
            item_name = (
                ui.input(placeholder="Example: Rent, Paycheck, etc.")
                .classes("w-3/4 m-auto")
                .on("blur", lambda: enable_next(item_budget))
            )
            item_name.disable()
            # Category Budgeted Amount
            ui.label("Budgeted Amount:").classes("text-xl m-auto")
            item_budget = (
                ui.number(
                    placeholder="Example: 400.00",
                    format="%.2f",
                    on_change=lambda: enable_next(item_name),
                )
                .classes("w-3/4 m-auto")
                .on("blur", lambda: (item_budget.update(), enable_next(save_button)))
            )
            item_budget.disable()

            ui.label()
            save_button = ui.button(
                "Save",
                on_click=lambda: (
                    save_category_item(
                        name=item_name,
                        budget=budget,
                        category_name=category_select,
                        budgeted_amount=item_budget,
                    ),
                    create_category_item_form.refresh(),
                ),
            ).classes("w-1/2 mx-auto")
            save_button.disable()
