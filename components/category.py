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
    get_all_budgets,
)
from constants import TRANSACTION_COLUMNS


@ui.refreshable
def spending_breakdown_chart() -> None:
    if not get_all_budgets():
        ui.label("No Budget Data")
    else:
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
                    dict(
                        text="Budgeted", x=0.185, y=0.5, font_size=16, showarrow=False
                    ),
                    dict(text="Actual", x=0.805, y=0.5, font_size=16, showarrow=False),
                ],
            )

            ui.plotly(fig)


@ui.refreshable
def category_treemap() -> None:
    if not get_all_budgets():
        ui.label("No Budget Data")
    else:
        budget = get_budget_data_by_date(
            budget_id=state.viz_budget_id,
            start_date=state.viz_start_date,
            end_date=state.viz_end_date,
        )
        category_items = [
            category_item
            for category in budget.categories
            for category_item in category.category_items
        ]
        categories_dict = {category.id: category.name for category in budget.categories}

        # List of Category Items to use in the Treemap
        category_items_list = [
            {
                "id": category_item.id,
                "label": category_item.name,
                "budgeted": category_item.budgeted,
                "actual": category_item.actual,
                "parent": categories_dict.get(category_item.category_id),
            }
            for category_item in category_items
        ]

        # Creating the root node of the treemap
        category_items_list.insert(
            0,
            {
                "id": "Category",
                "label": budget.name,
                "budgeted": None,
                "actual": 0.0,
                "parent": None,
            },
        )

        # Creating the parents of the category items (the categories they belong to) and nesting them in the budget
        for category in budget.categories:
            category_items_list.insert(
                1,
                {
                    "id": category.name,
                    "label": category.name,
                    "budgeted": None,
                    "actual": 0.0,
                    "parent": "Category",
                },
            )

        # Convert data into dataframe
        category_items_df = pd.DataFrame(category_items_list)

        fig = go.Figure(
            go.Treemap(
                ids=category_items_df.id,
                labels=category_items_df.label,
                parents=category_items_df.parent,
                values=category_items_df.actual,
                root_color="lightgrey",
                maxdepth=3,
            )
        )

        # Set the background color to black
        fig.update_layout(
            plot_bgcolor="#1d1d1d",
            paper_bgcolor="#1d1d1d",
            font={"color": "white"},
            title=f"Budget Composition: {state.viz_start_date} - {state.viz_end_date}",
            margin=dict(t=50, l=50, r=50, b=50),
        )

        ui.plotly(fig)
