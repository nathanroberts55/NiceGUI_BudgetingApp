from nicegui import ui
import pandas as pd
import random
from typing import List
from datetime import datetime, timedelta, timezone
from utils import okay, warn, error, generate_random_float, parse_date, to_dict
from sqlmodel import SQLModel, Session, create_engine, select, cast, DateTime
from .budget_model import Budget
from .category_model import Category
from .catergory_items_model import CategoryItem
from .transactions_model import Transaction

sqlite_file_name = "budget.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

session = Session(engine)


def initialize_database() -> None:
    print("Initializing Database...")
    SQLModel.metadata.create_all(engine)


def initialize_budget(name: str) -> None:
    # Current Date to be used in the default Budget Name
    # current_date = datetime.now().strftime("%m/%d/%Y")

    # Create a Budget
    budget: Budget = Budget.create(session=session, name=name)

    # Create the default categories
    income: Category = Category.create(
        session=session, name="Income", budget_id=budget.id
    )
    expense: Category = Category.create(
        session=session, name="Expense", budget_id=budget.id
    )
    spending: Category = Category.create(
        session=session, name="Spending", budget_id=budget.id
    )
    debt: Category = Category.create(session=session, name="Debt", budget_id=budget.id)
    saving: Category = Category.create(
        session=session, name="Saving", budget_id=budget.id
    )


def create_sample_data() -> None:
    print("Creating Sample Data...")
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
        # Income
        msft_1 = CategoryItem.create(
            session=session,
            name="MSFT Paycheck 1",
            budgeted="2677.58",
            category_id=income_id,
        )
        msft_2 = CategoryItem.create(
            session=session,
            name="MSFT Paycheck 2",
            budgeted="2677.58",
            category_id=income_id,
        )
        msft_2 = CategoryItem.create(
            session=session, name="Misc. Income", budgeted="0.00", category_id=income_id
        )
        # Expenses
        phone = CategoryItem.create(
            session=session, name="Phone", budgeted="80.00", category_id=expense_id
        )
        rent = CategoryItem.create(
            session=session, name="Rent", budgeted="1750.00", category_id=expense_id
        )
        gas = CategoryItem.create(
            session=session, name="Gas", budgeted="150.00", category_id=expense_id
        )
        yt_prem = CategoryItem.create(
            session=session,
            name="Youtube Premium",
            budgeted="11.99",
            category_id=expense_id,
        )
        adobe = CategoryItem.create(
            session=session, name="Adobe", budgeted="9.99", category_id=expense_id
        )
        disney = CategoryItem.create(
            session=session, name="Disney+", budgeted="9.99", category_id=expense_id
        )
        car_insurance = CategoryItem.create(
            session=session,
            name="Car Insurance",
            budgeted="0.00",
            category_id=expense_id,
        )
        utilities = CategoryItem.create(
            session=session, name="Utilities", budgeted="200.00", category_id=expense_id
        )
        groceries = CategoryItem.create(
            session=session, name="Groceries", budgeted="350.00", category_id=expense_id
        )
        rental_insurance = CategoryItem.create(
            session=session,
            name="Rental Insurance",
            budgeted="0.00",
            category_id=expense_id,
        )
        misc_expenses = CategoryItem.create(
            session=session,
            name="Misc. Expenses",
            budgeted="20.00",
            category_id=expense_id,
        )
        # Spending
        entertainment = CategoryItem.create(
            session=session,
            name="Entertainment",
            budgeted="450.00",
            category_id=spending_id,
        )
        dining_out = CategoryItem.create(
            session=session,
            name="Dining Out",
            budgeted="250.00",
            category_id=spending_id,
        )
        misc_spending = CategoryItem.create(
            session=session,
            name="Misc. Spending",
            budgeted="450.00",
            category_id=spending_id,
        )

        # Debt

        # Saving
        ira = CategoryItem.create(
            session=session, name="Roth IRA", budgeted="400.00", category_id=saving_id
        )
        savings = CategoryItem.create(
            session=session, name="Savings", budgeted="800.00", category_id=saving_id
        )
        investments = CategoryItem.create(
            session=session,
            name="Investments",
            budgeted="800.00",
            category_id=saving_id,
        )


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


def get_budget_data_by_date(budget_id: int, start_date: str, end_date: str) -> Budget:
    """
    Retrieves a Budget object with the given budget_id from the database and filters its transactions to only include those with a transaction_date between start_date and end_date.

    :param budget_id: The id of the budget to retrieve from the database.
    :type budget_id: int
    :param start_date: The start date of the date range to filter transactions by.
    :type start_date: str
    :param end_date: The end date of the date range to filter transactions by.
    :type end_date: str
    :return: A Budget object with filtered transactions.
    :rtype: Budget
    """
    # Convert start_date and end_date to datetime objects
    start_date_dt = datetime.strptime(start_date, "%m/%d/%y")
    end_date_dt = datetime.strptime(end_date, "%m/%d/%y")

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
                transactions = []
                for transaction in category_item.transactions:
                    if transaction.transaction_date:
                        # Convert transaction_date to datetime object
                        transaction_date_dt = datetime.strptime(
                            transaction.transaction_date, "%m/%d/%y"
                        )
                        if start_date_dt <= transaction_date_dt <= end_date_dt:
                            transactions.append(transaction)
                category_item.transactions = transactions
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


def get_budget_by_id(budget_id: int) -> Budget:
    """_summary_

    Args:
        budget_id (int): id of the Budget to be searched for

    Returns:
        Budget: First Budget object returned from database
    """
    with session:
        budget = session.exec(select(Budget).where(Budget.id == budget_id)).first()
    return budget


def update_budget_by_id(
    budget_id: int,
    name: str,
) -> None:
    with session:
        budget = session.exec(select(Budget).where(Budget.id == budget_id)).first()

        budget.name = name
        budget.updated = datetime.now(timezone.utc)

        session.add(budget)
        session.commit()
        session.refresh(budget)


def delete_budget_by_id(
    budget_id: int,
) -> None:
    with session:
        budget = session.exec(select(Budget).where(Budget.id == budget_id)).one()

        session.delete(budget)
        session.commit()


def get_all_categories() -> List[Category]:
    """Function that queries the database and returns all the Categories.
    Returns:
        List of Categories
    """
    with session:
        category = session.exec(select(Category)).all()

    return category


def get_category_by_id(category_id: int) -> None:
    with session:
        category = session.exec(
            select(Category).where(Category.id == category_id)
        ).first()

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


def get_category_data_by_date(
    category_id: int, start_date: str, end_date: str
) -> Category:
    """
    This function takes a category_id as an argument and returns a Category object with its related data.
    :param category_id: The id of the Category to retrieve.
    :param start_date: The start date of the date range to filter transactions by.
    :param end_date: The end date of the date range to filter transactions by.
    :return: A Category object with its related data.
    """
    # Convert start_date and end_date to datetime objects
    start_date_dt = datetime.strptime(start_date, "%m/%d/%y")
    end_date_dt = datetime.strptime(end_date, "%m/%d/%y")

    with session:
        # Get the category with the given id
        category = session.get(Category, category_id)
        # Access the category_items relationship attribute to get the related category items
        category_items = category.category_items
        for category_item in category_items:
            # Access the transactions relationship attribute to get the related transactions
            transactions = []
            for transaction in category_item.transactions:
                if transaction.transaction_date:
                    # Convert transaction_date to datetime object
                    transaction_date_dt = datetime.strptime(
                        transaction.transaction_date, "%m/%d/%y"
                    )
                    if start_date_dt <= transaction_date_dt <= end_date_dt:
                        transactions.append(transaction)
            category_item.transactions = transactions
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
        # Access the transactions relationship attribute to get the related transactions
        transactions = category_item.transactions
        return category_item


def get_category_item_by_id(category_item_id) -> CategoryItem:
    with session:
        return session.get(CategoryItem, category_item_id)


def get_all_transactions() -> List[Transaction]:
    """Function that queries the database and returns all the Transactions.
    Returns:
        List of Transactions
    """
    with session:
        transactions = session.exec(select(Transaction)).all()

    return transactions


def get_transactions_by_date(start_date: str, end_date: str) -> List[Transaction]:
    """
    Retrieves transactions from the database and filters them to only include those with a transaction_date between start_date and end_date.

    :param start_date: The start date of the date range to filter transactions by.
    :type start_date: str
    :param end_date: The end date of the date range to filter transactions by.
    :type end_date: str
    :return: A list of filtered transactions.
    :rtype: List[Transaction]
    """
    # Convert start_date and end_date to datetime objects
    start_date_dt = datetime.strptime(start_date, "%m/%d/%y")
    end_date_dt = datetime.strptime(end_date, "%m/%d/%y")

    with session:
        # Access the transactions relationship attribute to get the related transactions
        statement = select(Transaction)
        result = session.exec(statement)
        transactions = result.all()

        # Filter transactions by date range
        filtered_transactions = [
            transaction
            for transaction in transactions
            if transaction.transaction_date
            and start_date_dt
            <= datetime.strptime(transaction.transaction_date, "%m/%d/%y")
            <= end_date_dt
        ]

        return filtered_transactions


def get_transaction_by_id(transaction_id) -> Transaction:
    with session:
        return session.get(Transaction, transaction_id)


def update_transaction_by_id(
    transaction_id: int,
    name: str,
    transaction_date: str,
    amount: str,
    category_item_id: int,
) -> None:
    with session:
        transaction = session.exec(
            select(Transaction).where(Transaction.id == transaction_id)
        ).first()

        transaction.name = name
        transaction.transaction_date = transaction_date
        transaction.amount = amount
        transaction.category_item_id = category_item_id
        transaction.updated = datetime.now(timezone.utc)

        session.add(transaction)
        session.commit()
        session.refresh(transaction)


def delete_transaction_by_id(transaction_id: int) -> None:
    with session:
        transaction = session.exec(
            select(Transaction).where(Transaction.id == transaction_id)
        ).one()
        session.delete(transaction)
        session.commit()


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


def create_category_item(name: str, category_name: str, budgeted_amount: str) -> None:
    """Saves a new category item to the database.

    This method is called when the Category Item form is submitted. It creates a new Category Item and commits it to the database.

    Args:
        name (ui.input): The name of the new category item.
        budget (Budget): The budget object associated with the new category item.
        category_name (ui.select): The name of the category associated with the new category item.
        budgeted_amount (ui.number): The budgeted amount for the new category item.
        budget_name (ui.button):
    """

    with session:
        category = session.exec(
            select(Category).where(Category.name == category_name)
        ).first()

        new_item = CategoryItem.create(
            session=session,
            name=name,
            budgeted=budgeted_amount,
            category_id=category.id,
        )


def update_category_item_by_id(
    category_item_id: int,
    name: str,
    category_name: str,
    budgeted_amount: str,
) -> None:
    with session:
        category_item = session.exec(
            select(CategoryItem).where(CategoryItem.id == category_item_id)
        ).first()

        category = session.exec(
            select(Category).where(Category.name == category_name)
        ).first()

        category_item.name = name
        category_item.category_id = category.id
        category_item.budgeted = budgeted_amount
        category_item.updated = datetime.now(timezone.utc)

        session.add(category_item)
        session.commit()
        session.refresh(category_item)


def delete_category_item_by_id(category_item_id: int) -> None:
    with session:
        category_item = session.exec(
            select(CategoryItem).where(CategoryItem.id == category_item_id)
        ).one()
        session.delete(category_item)
        session.commit()


def create_transaction(
    name: str,
    transaction_date: str,
    amount: str,
    category_item_id: int,
) -> None:
    """Function to save transaction to the database

    Args:
        name (ui.input): string name of the transaction
        transaction_date (ui.input): string representation of when the transaction occured
        category_item_name (ui.select): name of the category item that the transaction is under
        amount (ui.number): ztring representation of the dollar amount of the transaction
    """
    # # Convert the transaction_date string to a datetime object
    # try:
    #     transaction_date_dt = datetime.strptime(transaction_date, "%m/%d/%y").replace(
    #         tzinfo=timezone.utc
    #     )
    # except ValueError as e:
    #     print(f"Error parsing date: {e}")
    #     return

    with session:
        # category_item: CategoryItem = session.exec(
        #     select(CategoryItem).where(CategoryItem.name == category_item_name)
        # ).first()

        transaction = Transaction(
            name=name,
            transaction_date=transaction_date,
            category_item_id=category_item_id,
            amount=amount,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)


def create_recurring_transactions(
    frequency: str, start_date: str, end_date: str, days_of_month: list
):
    """
    Create recurring transaction records in a database.

    :param frequency: The frequency of the recurring transactions. Options are "Weekly", "Bi-Weekly", "Monthly", "Twice a Month", and "Annually".
    :param start_date: The start date for the recurring transactions in the format 'YYYY-MM-DD'.
    :param end_date: The end date for the recurring transactions in the format 'YYYY-MM-DD'.
    :param days_of_month: A list of integers representing the days of the month on which a transaction may occur.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current_date = start
    last_transaction_date = None
    while current_date <= end:
        if frequency == "Weekly" and current_date.day in days_of_month:
            if (
                last_transaction_date is None
                or (current_date - last_transaction_date).days >= 7
            ):
                # Create new record in database for current_date
                last_transaction_date = current_date
        elif frequency == "Bi-Weekly" and current_date.day in days_of_month:
            if (
                last_transaction_date is None
                or (current_date - last_transaction_date).days >= 14
            ):
                # Create new record in database for current_date
                last_transaction_date = current_date
        elif frequency == "Monthly" and current_date.day in days_of_month:
            if (
                last_transaction_date is None
                or (current_date - last_transaction_date).days >= 28
            ):
                # Create new record in database for current_date
                last_transaction_date = current_date
        elif frequency == "Twice a Month" and current_date.day in days_of_month:
            if last_transaction_date is None or (
                current_date.month != last_transaction_date.month
            ):
                # Create new record in database for current_date
                last_transaction_date = current_date
        elif frequency == "Annually" and current_date.day in days_of_month:
            if (
                last_transaction_date is None
                or (current_date - last_transaction_date).days >= 364
            ):
                # Create new record in database for current_date
                last_transaction_date = current_date
        current_date += timedelta(days=1)
