from nicegui import ui
from constants import INCOME_TABLE_COLUMNS, EXPENSE_TABLE_COLUMNS, RECURRING_OPTIONS
from database import save_income, save_expense, get_transactions


@ui.refreshable
def transactions_tables(ledger) -> None:
    income_transactions, expense_transactions = get_transactions(ledger)
    # Income Table
    ui.label('Income Table').classes('text-4xl my-5')
    if income_transactions:
        ui.table(columns=INCOME_TABLE_COLUMNS, rows=income_transactions, row_key='name').classes('mb-10')
        ui.label(f"Total Income: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in income_transactions))}").classes('text-right')
    else:
        ui.label('No Income to Show').classes('text-semibold text-xl')

    # Expense Table
    ui.markdown('Expense Table').classes('text-4xl my-5')
    if expense_transactions:
        ui.table(
            columns=EXPENSE_TABLE_COLUMNS, 
            rows=expense_transactions, 
            row_key='name').classes('mb-10')
        ui.label(f"Total Expenses: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in expense_transactions))}").classes('text-right')
    else:
        ui.label('No Expenses to Show').classes('text-semibold text-xl')

@ui.refreshable
def income_entry(ledger) -> None:
    income_transactions, _ = get_transactions(ledger)
    # Income Entry
    income_autocomplete_options = [transaction.source for transaction in income_transactions]
    with ui.column():
        ui.label('Income Entry').classes('text-semibold text-3xl my-5')
        with ui.input('Income Date') as income_date:
            with ui.menu() as menu:
                ui.date().bind_value(income_date)
            with income_date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
        income_source = ui.input(label='Income Source', autocomplete=income_autocomplete_options)
        income_amount = ui.number(label='Income Amount', value=0.00, format='%.2f')
        ui.button(text='Submit', on_click=lambda: (save_income(ledger, income_date, income_source, income_amount), income_entry.refresh()))

@ui.refreshable
def expense_entry(ledger):
    _, expense_transactions = get_transactions(ledger)
    expense_autocomplete_options = [transaction.source for transaction in expense_transactions]
    with ui.column():
        ui.label('Expense Entry').classes('text-semibold text-3xl my-5')
        with ui.input('Expense Date') as expense_date:
            with ui.menu() as menu:
                ui.date().bind_value(expense_date)
            with expense_date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
        expense_source = ui.input(label='Expense Source', autocomplete=expense_autocomplete_options)
        expense_amount = ui.number(label='Expense Amount', value=0.00, format='%.2f')
        expense_recuring = ui.switch('Recuring Expense')
        expense_recurring_frequency = ui.select(RECURRING_OPTIONS, label='Frequency', value=RECURRING_OPTIONS[0]).bind_visibility_from(expense_recuring, 'value').classes('ml-10 w-36')
        expense_recurring_dates = ui.select([day for day in range(1,32)], multiple=True, value=1, label='Day').bind_visibility_from(expense_recuring, 'value').props('use-chips').classes('ml-10 w-36')
        ui.button(text='Submit', on_click= lambda: (save_expense(ledger, expense_date, expense_source, expense_amount), expense_entry.refresh()))
