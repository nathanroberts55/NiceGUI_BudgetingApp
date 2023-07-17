TRANSACTION_COLUMNS = [
    {
        "name": "transaction_date",
        "label": "Date",
        "field": "transaction_date",
        "sortable": True,
        "align": "left",
    },
    {
        "name": "name",
        "label": "Name",
        "field": "name",
        "required": True,
        "align": "left",
    },
    {
        "name": "amount",
        "label": "Amount",
        "field": "amount",
        "sortable": True,
        ":format": 'value => "$" + value',
    },
]

RECURRING_OPTIONS = ["Weekly", "Bi-Weekly", "Monthly", "Twice a Month"]
