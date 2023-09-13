import os
from database.db import initialize_database, create_sample_data

# Initialize the SQLite Database
if not os.path.exists("budget.db"):
    print("Database does not exist... Creating Database")
    initialize_database()
    create_sample_data()

from nicegui import app, ui
from components import transaction, budget, category, category_item, common


ui.dark_mode().enable()

with ui.tabs().classes("w-full") as tabs:
    budget_planning = ui.tab("Budget Planning", icon="edit_document").classes("w-40")
    budget_report = ui.tab("Budget Reporting", icon="table_view").classes("w-40")
    budget_viz = ui.tab("Budget Visualization", icon="insights").classes("w-40")
with ui.tab_panels(tabs, value=budget_planning).classes("w-full"):
    with ui.tab_panel(budget_planning):
        budget.budget_grid()

    with ui.tab_panel(budget_report):
        common.reporting_budget_date_select()
        budget.budget_breakdown()
        category_item.category_item_grid()
        transaction.transaction_grid()

    with ui.tab_panel(budget_viz):
        common.viz_budget_date_select()
        budget.budget_guage()
        transaction.transactions_over_time_chart()
        category.spending_breakdown_chart()
        category.category_treemap()

ui.run(title="Budgeting App", favicon="assets\\budgeting.png")
