INCOME_TABLE_COLUMNS = [
        {'name': 'date', 'label': 'Date', 'field': 'date', 'sortable': True},
        {'name': 'source', 'label': 'Income Source', 'field': 'source', 'required': True, 'align': 'left'},
        {'name': 'amount', 'label': 'Amount', 'field': 'amount', 'sortable': True, ':format': 'value => "$" + value'},
    ]

EXPENSE_TABLE_COLUMNS = [
        {
            'name': 'date',
            'label': 'Date',
            'field': 'date', 
            'required': True, 
            'sortable': True
        },
        {
            'name': 'source', 
            'label': 'Expense Source', 
            'field': 'source', 
            'required': True, 
            'align': 'left'
        },
        {
            'name': 'amount', 
            'label': 'Amount', 
            'field': 'amount',
            'required': True, 
            'sortable': True,
            ':format': 'value => "$" + value'
        },
    ]

RECURRING_OPTIONS = ['Weekly', 'Bi-Weekly', 'Monthly', 'Twice a Month']