from nicegui import ui
from utils import enable_next, to_dict
from components import budget, state
from database.db import (
    get_all_category_items,
    delete_category_item_by_id,
    get_category_by_id,
    update_category_item_by_id,
    get_all_categories,
    create_category_item,
)


category_select: ui.select = None
item_name: ui.input = None
item_budget: ui.number = None
save_button: ui.button = None
grid: ui.aggrid = None


def add_category_item() -> None:
    create_category_item(
        name=add_item_name.value,
        category_name=add_category_select.value,
        budgeted_amount=f"{float(add_item_budget.value):.2f}",
    )

    grid.options["rowData"] = sorted(
        to_dict(get_all_category_items()),
        key=lambda data: data["name"],
    )

    add_dialog.close()

    ui.notify(f"Successfully Saved {add_item_name.value}", color="Green")

    add_item_name.set_value(None)
    add_category_select.set_value(None)
    add_item_budget.set_value(None)

    grid.update()
    budget.budget_breakdown.refresh()


def update_category_item() -> None:
    update_category_item_by_id(
        category_item_id=state.selected_category_item["id"],
        name=edit_item_name.value,
        category_name=edit_category_select.value,
        budgeted_amount=f"{float(edit_item_budget.value):.2f}",
    )

    grid.options["rowData"] = sorted(
        to_dict(get_all_category_items()),
        key=lambda data: data["name"],
    )

    ui.notify(f"Successfully Updated {edit_item_name.value}")

    edit_dialog.close()
    grid.update()
    budget.budget_breakdown.refresh()


with ui.dialog() as add_dialog:
    with ui.card():
        # Category Select
        add_category_select = ui.select(
            [category.name for category in get_all_categories()],
            label="Select a Category",
        ).classes("w-full m-auto")
        # Category Item Name
        add_item_name = ui.input(
            label="Category Item Name", placeholder="Example: Rent"
        ).classes("w-full m-auto")
        # Category Budgeted Amount
        add_item_budget = (
            ui.number(
                label="Category Item Budget",
                placeholder="Example: 400.00",
                format="%.2f",
            )
            .classes("w-full m-auto")
            .on("blur", lambda: add_item_budget.update())
        )
        ui.button("Save Category Item", on_click=add_category_item).classes("m-auto")

with ui.dialog() as edit_dialog:
    with ui.card():
        # Category Select
        edit_category_select = ui.select(
            [category.name for category in get_all_categories()],
            label="Select a Category",
        ).classes("w-full m-auto")
        # Category Item Name
        edit_item_name = ui.input(
            label="Category Item Name", placeholder="Example: Rent, Paycheck, etc."
        ).classes("w-full m-auto")
        # Category Budgeted Amount
        edit_item_budget = (
            ui.number(
                label="Category Item Budget",
                placeholder="Example: 400.00",
                format="%.2f",
            )
            .classes("w-full m-auto")
            .on("blur", lambda: edit_item_budget.update())
        )
        ui.button("Edit Category Item", on_click=update_category_item).classes("m-auto")


def open_add_dialog() -> None:
    # Open the Add Transaction dialog
    add_dialog.open()


async def open_edit_dialog() -> None:
    state.selected_category_item = await grid.get_selected_row()

    if not state.selected_category_item:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    category = get_category_by_id(state.selected_category_item["category_id"])

    edit_category_select.set_value(category.name)
    edit_item_name.set_value(state.selected_category_item["name"])
    edit_item_budget.set_value(state.selected_category_item["budgeted"])

    edit_dialog.open()


async def delete_category_item() -> None:
    row = await grid.get_selected_row()

    if not row:
        ui.notify("No Row Selected. Please select and try again.", color="Red")
        return

    delete_category_item_by_id(row["id"])

    grid.options["rowData"] = sorted(
        to_dict(get_all_category_items()),
        key=lambda data: data["name"],
    )

    grid.update()
    budget.budget_breakdown.refresh()

    ui.notify(f"Successfully Deleted {row['name']}", color="Red")


@ui.refreshable
def category_item_grid() -> None:
    global grid
    category_items = get_all_category_items()
    category_items_list = to_dict(category_items)

    with ui.expansion("Category Item Table").classes("text-2xl mt-6 mb-2"):
        grid = ui.aggrid(
            {
                "defaultColDef": {"flex": 1},
                "columnDefs": [
                    {"headerName": "ID", "field": "id", "hide": True},
                    {"headerName": "Created", "field": "created", "hide": True},
                    {"headerName": "Updated", "field": "updated", "hide": True},
                    {"headerName": "Category ID", "field": "category_id", "hide": True},
                    {
                        "headerName": "Name",
                        "field": "name",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                    {
                        "headerName": "Budgeted Amount",
                        "field": "budgeted",
                        "valueFormatter": "'$' + value",
                        "filter": "agTextColumnFilter",
                        "floatingFilter": True,
                    },
                ],
                "rowData": sorted(category_items_list, key=lambda data: data["name"]),
                "rowSelection": "single",
            }
        ).classes("max-h-92")

        with ui.row().classes("mt-4"):
            ui.button("Add", color="Green", on_click=open_add_dialog)
            ui.button("Edit", on_click=open_edit_dialog)
            ui.button("Delete", color="Red", on_click=delete_category_item)
