from nicegui import app, ui
import os
from datetime import datetime
from components import expense, income, transaction, budget, category, category_item
import plotly.graph_objects as go
from database.db import initialize_database, create_sample_data

# Initialize the SQLite Database
if not os.path.exists("budget.db"):
    print("Database does not exist... Creating Database")
    initialize_database()
    create_sample_data()


ui.dark_mode().enable()

with ui.tabs().classes("w-full") as tabs:
    budget_planning = ui.tab("Budget Planning", icon="edit_document").classes("w-40")
    budget_entry = ui.tab("Budget Entry", icon="note_add").classes("w-40")
    budget_report = ui.tab("Budget Reporting", icon="table_view").classes("w-40")
    budget_viz = (
        ui.tab("Budget Visualization", icon="insights")
        # .on("blur", update_data)
        .classes("w-40")
    )
with ui.tab_panels(tabs, value=budget_planning).classes("w-full"):
    with ui.tab_panel(budget_planning):
        # budget.create_budget_form()
        category_item.create_category_item_form()
        transaction.create_transaction_form()

    with ui.tab_panel(budget_entry):
        with ui.row().classes("w-full"):
            income.income_entry()
            expense.expense_entry()

    with ui.tab_panel(budget_report):
        budget.budget_breakdown()
        category.transactions_tables_by_category()

    with ui.tab_panel(budget_viz):
        ui.label("Data Visualizations Coming Soon!")

ui.run(title="Budgeting App")
