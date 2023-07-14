from nicegui import ui
import pandas as pd
from typing import List
from datetime import datetime
from utils import okay, warn, error
from sqlmodel import SQLModel, Session, create_engine, select
from database.models import (
    Budget,
    Category,
    DebtCategory,
    SavingCategory,
    CategoryItem,
    Transaction,
)

sqlite_file_name = "budget.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

session = Session(engine)


def initialize_database() -> None:
    SQLModel.metadata.create_all(engine)


def create_sample_data() -> None:
    with session:
        okay("Creating Budget Record")
        budget = Budget()
        session.add(budget)
        okay("Saving Budget Record")
        session.commit()
        okay("Saved Budget Record")

        okay("Getting Budget Record")
        budget_id = session.exec(select(Budget)).first().id

        if not budget_id:
            error("No Budget Id Found, ending execution")
            return

        warn("Budget Record Id:", budget_id)

        okay("Creating Category Records")
        income = Category(name="Income", budget_id=budget_id)
        expense = Category(name="Expense", budget_id=budget_id)
        spending = Category(name="Spending", budget_id=budget_id)
        debt = Category(name="Debt", budget_id=budget_id)
        saving = Category(name="Saving", budget_id=budget_id)

        session.add(income)
        session.add(expense)
        session.add(spending)
        session.add(debt)
        session.add(saving)
        okay("Saving Category Records")
        session.commit()
        okay("Saved Category Records")

        okay("Getting the ID's for the 4 categories created")
        income_id = (
            session.exec(select(Category).where(Category.name == "Income")).first().id
        )
        expense_id = (
            session.exec(select(Category).where(Category.name == "Expense")).first().id
        )
        spending_id = (
            session.exec(select(Category).where(Category.name == "Spending")).first().id
        )
        debt_id = (
            session.exec(select(Category).where(Category.name == "Debt")).first().id
        )
        saving_id = (
            session.exec(select(Category).where(Category.name == "Saving")).first().id
        )

        okay("Collected the Category Id's")
        warn("Category | Income ID:", income_id)
        warn("Category | Expense ID:", expense_id)
        warn("Category | Spending ID:", spending_id)
        warn("Category | Debt ID:", debt_id)
        warn("Category | Saving ID:", saving_id)

        okay("Creating Category Items")
        job_income = CategoryItem(name="Uber Paycheck", category_id=income_id)
        rent = CategoryItem(name="Rent", category_id=expense_id)
        groceries = CategoryItem(name="Groceries", category_id=expense_id)
        credit_card = CategoryItem(name="Chase Credit Card", category_id=debt_id)
        credit_union = CategoryItem(name="Mission FCU", category_id=saving_id)

        session.add(job_income)
        session.add(rent)
        session.add(groceries)
        session.add(credit_card)
        session.add(credit_union)
        okay("Saving Category Items")
        session.commit()
        okay("Saved Category Items")

        okay("Getting the ID's for the 5 category items created")
        job_income_id = (
            session.exec(
                select(CategoryItem).where(CategoryItem.name == "Uber Paycheck")
            )
            .first()
            .id
        )
        rent_id = (
            session.exec(select(CategoryItem).where(CategoryItem.name == "Rent"))
            .first()
            .id
        )
        groceries_id = (
            session.exec(select(CategoryItem).where(CategoryItem.name == "Groceries"))
            .first()
            .id
        )
        credit_card_id = (
            session.exec(
                select(CategoryItem).where(CategoryItem.name == "Chase Credit Card")
            )
            .first()
            .id
        )
        credit_union_id = (
            session.exec(select(CategoryItem).where(CategoryItem.name == "Mission FCU"))
            .first()
            .id
        )

        okay("Collected the Category Item Id's")
        warn("CategoryItem | Job Income ID:", job_income_id)
        warn("CategoryItem | Rent ID:", rent_id)
        warn("CategoryItem | Groceries ID:", groceries_id)
        warn("CategoryItem | Chase Credit Card ID:", credit_card_id)
        warn("CategoryItem | Mission FCU ID:", credit_union_id)


def get_all_budgets() -> List[Budget]:
    """Function that queries the database and returns all the Budgets.
    Returns:
        List of Budgets
    """
    with session:
        budget = session.execute(select(Budget)).all()

    return budget


def get_all_categories() -> List[Category]:
    """Function that queries the database and returns all the Categories.
    Returns:
        List of Categories
    """
    with session:
        category = session.execute(select(Category)).all()

    return category


def get_all_category_items() -> List[CategoryItem]:
    """Function that queries the database and returns all the CategoryItems.
    Returns:
        List of CategoryItems
    """
    with session:
        category_items = session.execute(select(CategoryItem)).all()

    return category_items


def get_all_transactions() -> List[Transaction]:
    """Function that queries the database and returns all the Transactions.
    Returns:
        List of Transactions
    """
    with session:
        transactions = session.execute(select(Transaction)).all()

    return transactions


# Data Visualization
def get_transaction_data() -> pd.DataFrame | None:
    """_summary_

    Returns:
        pd.DataFrame: Transactions in the form a pandas dataframe
    """

    return None


def save_income(income_date, income_source, income_amount) -> None:
    """When the Income form is submitted, create a transaction and commit to the database

    Args:
        income_date (datetime.datetime): Date the Transaction was posted
        income_source (str): Name of the Transaction
        income_amount (str): Amount of the Transaction
    """
    date = datetime.strptime(income_date.value, "%Y-%m-%d")

    with session:
        Transaction.add(
            session=session,
            name=income_source,
            date=date.strftime("%m/%d/%y"),
            amount=income_amount,
        )
        session.commit()

    ui.notify(f"{income_source.value} Saved!")


def save_expense(expense_date, expense_source, expense_amount) -> None:
    """When the Income form is submitted, create a transaction and commit to the database

    Args:
        expense_date (datetime.datetime): Date the Transaction was posted
        expense_source (str): Name of the Transaction
        expense_amount (str): Amount of the Transaction
    """
    date = datetime.strptime(expense_date.value, "%Y-%m-%d")

    expense = Transaction(
        name=expense_source,
        date=date.strftime("%m/%d/%y"),
        amount=expense_amount,
    )

    with session:
        session.add(expense)
        session.commit()

    ui.notify(f"{expense_source.value} Saved!")
