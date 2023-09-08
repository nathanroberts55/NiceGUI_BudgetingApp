import pandas as pd
from nicegui import ui
from utils import to_dict
from components import state
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from database.db import (
    get_category_data_by_date,
    get_all_categories,
    get_budget_data_by_date,
)
from constants import TRANSACTION_COLUMNS


def category_list() -> None:
    categories = get_all_categories()
    for category in categories:
        ui.label(category.name)


@ui.refreshable
def transactions_tables_by_category() -> None:
    category_ids = [category.id for category in get_all_categories()]

    for id in category_ids:
        category = get_category_data_by_date(
            category_id=id,
            start_date=state.reporting_start_date,
            end_date=state.reporting_end_date,
        )
        transactions = [
            transaction
            for category_item in category.category_items
            for transaction in category_item.transactions
        ]
        if transactions:
            transactions_list = to_dict(transactions)
            ui.label(f"{category.name} Transactions").classes("text-4xl my-5")
            ui.table(
                columns=TRANSACTION_COLUMNS, rows=transactions_list, row_key="name"
            ).classes("mb-10")
            ui.label(
                f"Total Transaction Volume: ${'{:.2f}'.format(sum(float(transaction.amount) for transaction in transactions))}"
            ).classes("text-right")
        else:
            ui.label(f"No {category.name} to Show").classes("text-semibold text-xl")


@ui.refreshable
def spending_breakdown_chart() -> None:
    budget = get_budget_data_by_date(
        budget_id=state.viz_budget_id,
        start_date=state.viz_start_date,
        end_date=state.viz_end_date,
    )

    data = [
        {
            "id": category.id,
            "name": category.name,
            "budget_id": category.budget_id,
            "budgeted_total": category.budgeted_total,
            "actual_total": category.actual_total,
            "percent_of_budget": category.percent_of_budget,
            "over_under": category.over_under,
        }
        for category in budget.categories
        if category.name != "Income"
    ]

    categories_df = pd.DataFrame(data)

    if not categories_df.empty:
        categories_df = categories_df.astype(
            {
                "id": "int",
                "name": "str",
                "budget_id": "int",
                "budgeted_total": "float",
                "actual_total": "float",
                "percent_of_budget": "float",
                "over_under": "float",
            }
        )

        fig = make_subplots(
            rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
        )
        fig.add_trace(
            go.Pie(
                labels=categories_df.name,
                values=categories_df.budgeted_total,
                name="Budgeted Expenses",
            ),
            1,
            1,
        )
        fig.add_trace(
            go.Pie(
                labels=categories_df.name,
                values=categories_df.actual_total,
                name="Actual Expenses",
            ),
            1,
            2,
        )

        # Use `hole` to create a donut-like pie chart
        fig.update_traces(hole=0.4, hoverinfo="label+percent+name")

        # Set the background color to black
        fig.update_layout(
            plot_bgcolor="#1d1d1d",
            paper_bgcolor="#1d1d1d",
            font={"color": "white"},
            title=f"Budgeted vs Actual Expenses: {state.viz_start_date} - {state.viz_end_date}",
            annotations=[
                dict(text="Budgeted", x=0.185, y=0.5, font_size=16, showarrow=False),
                dict(text="Actual", x=0.805, y=0.5, font_size=16, showarrow=False),
            ],
        )

        ui.plotly(fig)
