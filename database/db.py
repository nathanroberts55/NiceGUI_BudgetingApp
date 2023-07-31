from nicegui import ui
import pandas as pd
from typing import List
from datetime import datetime
from utils import okay, warn, error, generate_random_float
from sqlmodel import SQLModel, Session, create_engine, select
from .budget_model import Budget
from .category_model import Category
from .catergory_items_model import CategoryItem
from .transactions_model import Transaction

sqlite_file_name = "budget.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

session = Session(engine)


def initialize_database() -> None:
    SQLModel.metadata.create_all(engine)


def initialize_budget() -> None:
    # Current Date to be used in the default Budget Name
    current_date = datetime.now().strftime("%m/%d/%Y")

    # Create a Budget
    budget: Budget = Budget.create(name=f"Budget | {current_date}")

    # Create the default categories
    income: Category = Category.create(name="Income", budget_id=budget.id)
    expense: Category = Category.create(name="Expense", budget_id=budget.id)
    spending: Category = Category.create(name="Spending", budget_id=budget.id)
    debt: Category = Category.create(name="Debt", budget_id=budget.id)
    saving: Category = Category.create(name="Saving", budget_id=budget.id)


def create_sample_data() -> None:
    with session:
        okay("Creating Budget Record")
        budget = Budget(name="My First Budget")
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
        job_income = CategoryItem(
            name="Uber Paycheck", budgeted="4500.00", category_id=income_id
        )
        rent = CategoryItem(name="Rent", budgeted="800.00", category_id=expense_id)
        groceries = CategoryItem(
            name="Groceries", budgeted="300.00", category_id=expense_id
        )
        credit_card = CategoryItem(
            name="Chase Credit Card", budgeted="300.00", category_id=debt_id
        )
        credit_union = CategoryItem(
            name="Mission FCU", budgeted="500.00", category_id=saving_id
        )

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

        # Creating some sample transactions
        for transaction in range(0, 45):
            cat_item_id = (transaction % 5) + 1
            okay("Creating New Transaction, #", transaction)
            Transaction.add(
                session=session,
                name=f"Test Source: {transaction}",
                transaction_date=datetime.now().strftime("%m/%d/%y"),
                amount=generate_random_float(),
                category_item_id=cat_item_id,
            )
            okay("Saving New Transaction, #", transaction)
            session.commit()
            okay("Saved New Transaction, #", transaction)
        okay("All Transactions Created!")


def get_all_budgets() -> List[Budget]:
    """Function that queries the database and returns all the Budgets.
    Returns:
        List of Budgets
    """
    with session:
        budget = session.exec(select(Budget)).all()

    return budget


def get_budget_with_related_data(budget_id: int) -> Budget:
    """
    This function takes a budget_id as an argument and returns a Budget object with its related data.
    :param budget_id: The id of the budget to retrieve.
    :return: A Budget object with its related data.
    """
    with session:
        # Get the budget with the given id
        budget = session.get(Budget, budget_id)
        # Access the categories relationship attribute to get the related categories
        categories = budget.categories
        for category in categories:
            # Access the category_items relationship attribute to get the related category items
            category_items = category.category_items
            for category_item in category_items:
                # Access the transactions relationship attribute to get the related transactions
                transactions = category_item.transactions
        return budget


def get_budget_by_name(budget_name) -> Budget:
    """_summary_

    Args:
        budget_name (str): name of the Budget to be searched for

    Returns:
        Budget: First Budget object returned from database
    """
    with session:
        budget = session.exec(select(Budget).where(Budget.name == budget_name)).first()
    return budget


def get_all_categories() -> List[Category]:
    """Function that queries the database and returns all the Categories.
    Returns:
        List of Categories
    """
    with session:
        category = session.exec(select(Category)).all()

    return category


def get_category_with_related_data(category_id: int) -> Category:
    """
    This function takes a category_id as an argument and returns a Category object with its related data.
    :param category_id: The id of the Category to retrieve.
    :return: A Category object with its related data.
    """
    with session:
        # Get the category with the given id
        category = session.get(Category, category_id)
        # Access the categories relationship attribute to get the related category items
        category_items = category.category_items
        for category_item in category_items:
            # Access the transactions relationship attribute to get the related transactions
            transactions = category_item.transactions
        return category


def get_all_category_items() -> List[CategoryItem]:
    """Function that queries the database and returns all the CategoryItems.
    Returns:
        List of CategoryItems
    """
    with session:
        category_items = session.exec(select(CategoryItem)).all()

    return category_items


def get_category_items_with_related_data(category_item_id: int) -> CategoryItem:
    """
    This function takes a category_item_id as an argument and returns a CategoryItem object with its related data.
    :param category_item_id: The id of the CategoryItem to retrieve.
    :return: A CategoryItem object with its related data.
    """
    with session:
        # Get the category_item with the given id
        category_item = session.get(CategoryItem, category_item_id)
        # Access the transactions relationship attribute to get the related trnasactions
        transactions = category_item.transactions
        return category_item


def get_all_transactions() -> List[Transaction]:
    """Function that queries the database and returns all the Transactions.
    Returns:
        List of Transactions
    """
    with session:
        transactions = session.exec(select(Transaction)).all()

    return transactions


# Data Visualization
def get_transaction_data() -> pd.DataFrame | None:
    """_summary_

    Returns:
        pd.DataFrame: Transactions in the form a pandas dataframe
    """

    return None


def save_budget(budget_name: ui.input) -> None:
    """When the Budget form is submitted, create a transaction and commit to the database

    Args:
        budget_name (ui.button):
    """

    with session:
        budget: Budget = Budget.create(
            session=session,
            name=budget_name.value,
        )
        Category.add(session=session, name="Income", budget_id=budget.id)
        Category.add(session=session, name="Expense", budget_id=budget.id)
        Category.add(session=session, name="Spending", budget_id=budget.id)
        Category.add(session=session, name="Debt", budget_id=budget.id)
        Category.add(session=session, name="Saving", budget_id=budget.id)

        session.commit()

    ui.notify(f"{budget_name.value} Saved!")


def save_category_item(
    name: ui.input, budget: Budget, category_name: ui.select, budgeted_amount: ui.number
) -> None:
    """When the Budget form is submitted, create a transaction and commit to the database

    Args:
        budget_name (ui.button):
    """

    with session:
        CategoryItem.add(
            session=session,
            budget=budget.id,
            category_id=[
                category
                for category in budget.categories
                if category.name == category_name.value
            ][0].id,
            name=name.value,
            budgeted=budgeted_amount.value,
        )
        session.commit()

    ui.notify(f"{name.value} Saved!")


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
