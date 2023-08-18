from nicegui import app, ui
import os
from datetime import datetime
from components import (
    transaction,
    budget,
    category,
    category_item,
    common,
)
import plotly.graph_objects as go
from database.db import initialize_database, create_sample_data

# Initialize the SQLite Database
if not os.path.exists("budget.db"):
    print("Database does not exist... Creating Database")
    initialize_database()
    create_sample_data()


ui.dark_mode().enable()

with ui.tabs().classes("w-full") as tabs:
    # budget_planning = ui.tab("Budget Planning", icon="edit_document").classes("w-40")
    budget_report = ui.tab("Budget Reporting", icon="table_view").classes("w-40")
    budget_viz = (
        ui.tab("Budget Visualization", icon="insights")
        # .on("blur", update_data)
        .classes("w-40")
    )
with ui.tab_panels(tabs, value=budget_report).classes("w-full"):
    with ui.tab_panel(budget_report):
        common.budget_date_select()
        budget.budget_breakdown()
        transaction.transaction_grid()
        category_item.category_item_grid()

    with ui.tab_panel(budget_viz):
        ui.label("Data Visualizations Coming Soon!")

ui.run(title="Budgeting App", favicon="assets\\budgeting.png")
