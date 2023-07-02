from nicegui import app, ui
from datetime import datetime
from database import get_transaction_data, Ledger, TransactionType
from components import transactions_tables, income_entry, expense_entry
import plotly.graph_objects as go

ui.dark_mode().enable()
ledger = Ledger([transactions_tables.refresh])

# Make Chart
transaction_chart = go.Figure()
transaction_chart.update_layout(
    title_text='Budget Total Breakdown',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white')
)

# Plotting
def clear_trace():
    transaction_chart.data = []
    plot.update()

def add_trace() -> go.Figure:
    data = get_transaction_data(ledger)
    transaction_chart.add_trace(
        go.Bar(
            x=data.trans_type, 
            y=data.amount,
            marker_color=['red', 'green']
        )
    )

    return transaction_chart

            
def update_data():
    data = get_transaction_data(ledger)
    clear_trace()
    plot.clear()
    transaction_chart.add_trace(
        go.Bar(
            x=data.trans_type, 
            y=data.amount,
            marker_color=['red', 'green']
        )
    )
    plot.update()

ledger.save(datetime.now().strftime('%m/%d/%y'), TransactionType.INCOME, 'Salary', 1000.0)
ledger.save(datetime.now().strftime('%m/%d/%y'), TransactionType.INCOME, 'Bonus', 1500.0)
ledger.save(datetime.now().strftime('%m/%d/%y'), TransactionType.EXPENSE, 'Rent', 500.0)


with ui.tabs().classes('w-full') as tabs:
    data_entry = ui.tab('Data Entry', icon='note_add').classes('w-40')
    data_viz = ui.tab('Data Visualization', icon='insights').on('blur', update_data).classes('w-40')
with ui.tab_panels(tabs, value=data_entry).classes('w-full'):
    with ui.tab_panel(data_entry):
        with ui.row():
            income_entry(ledger)
            ui.splitter(horizontal=False).classes("my-10")
            expense_entry(ledger)
            # ui.splitter(horizontal=True).classes("my-10")
        

    with ui.tab_panel(data_viz):
        transactions_tables(ledger)
        ui.splitter(horizontal=True).classes("my-10")
        # Budget Visualizations
        # Get the data as a dataframe
        transaction_data = get_transaction_data(ledger)
        # UI Components
        ui.label('Budget Visualizations').classes('text-semibold text-3xl my-5')
        with ui.row():
            plot = ui.plotly(transaction_chart).classes('w-full h-100')
            update_data()
            # ui.button('Update', on_click=update_data)
        ui.splitter(horizontal=True).classes("my-10")

ui.run(title='Budgeting App')