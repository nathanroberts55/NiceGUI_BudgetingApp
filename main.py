from nicegui import app, ui
import os
from datetime import datetime

# from database.db import get_transaction_data
from components import expense, income, transaction
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
    data_viz = (
        ui.tab("Data Visualization", icon="insights")
        # .on("blur", update_data)
        .classes("w-40")
    )
with ui.tab_panels(tabs, value=data_entry).classes("w-full"):
    with ui.tab_panel(data_entry):
        with ui.row().classes("w-full"):
            income.income_entry()
            expense.expense_entry()

    with ui.tab_panel(data_viz):
        # transaction_tables.transactions_tables()
        ui.splitter(horizontal=True).classes("my-10")
        # Budget Visualizations
        # Get the data as a dataframe
        # transaction_data = get_transaction_data()
        # UI Components
        # ui.label("Budget Visualizations").classes("text-semibold text-3xl my-5")
        # with ui.row():
        # plot = ui.plotly(transaction_chart).classes("w-full h-100")
        # update_data()
        # ui.button('Update', on_click=update_data)
        # ui.splitter(horizontal=True).classes("my-10")

ui.run(title="Budgeting App")
