from nicegui import app, ui
import os
from datetime import datetime
from components import expense, income, transaction, budget, category
import plotly.graph_objects as go
from database.db import initialize_database, create_sample_data

# Initialize the SQLite Database
if not os.path.exists("budget.db"):
    print("Database does not exist... Creating Database")
    initialize_database()
    create_sample_data()


ui.dark_mode().enable()
# ledger = Ledger([transaction_tables.transactions_tables.refresh])

# # Make Chart
# transaction_chart = go.Figure()
# transaction_chart.update_layout(
#     title_text="Budget Total Breakdown",
#     plot_bgcolor="rgba(0,0,0,0)",
#     paper_bgcolor="rgba(0,0,0,0)",
#     font=dict(color="white"),
# )


# # Plotting
# def clear_trace():
#     transaction_chart.data = []
#     plot.update()


# def add_trace() -> go.Figure:
#     data = get_transaction_data()
#     transaction_chart.add_trace(
#         go.Bar(x=data.trans_type, y=data.amount, marker_color=["red", "green"])
#     )

#     return transaction_chart


# def update_data():
#     data = get_transaction_data()
#     clear_trace()
#     plot.clear()
#     transaction_chart.add_trace(
#         go.Bar(x=data.trans_type, y=data.amount, marker_color=["red", "green"])
#     )
#     plot.update()


with ui.tabs().classes("w-full") as tabs:
    data_entry = ui.tab("Data Entry", icon="note_add").classes("w-40")
    data_report = ui.tab("Data Reporting", icon="table_view").classes("w-40")
    data_viz = (
        ui.tab("Data Visualization", icon="insights")
        # .on("blur", update_data)
        .classes("w-40")
    )
with ui.tab_panels(tabs, value=data_report).classes("w-full"):
    with ui.tab_panel(data_entry):
        with ui.row().classes("w-full"):
            income.income_entry()
            expense.expense_entry()

    with ui.tab_panel(data_report):
        budget.budget_breakdown()
        category.transactions_tables_by_category()

    with ui.tab_panel(data_viz):
        ui.label("Data Visualizations Coming Soon!")

ui.run(title="Budgeting App")
