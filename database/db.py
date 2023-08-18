from nicegui import ui
import pandas as pd
import random
from typing import List
from datetime import datetime, timedelta
from utils import okay, warn, error, generate_random_float, parse_date
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
        for transaction in range(0, 100):
            # Get the current date
            today = datetime.now()

            # Define the range of days to choose from
            days_range = 365

            # Generate a random number of days within the range
            random_days = random.randint(0, days_range)

            # Subtract the random number of days from today to get a random date before today
            random_date = today - timedelta(days=random_days)

            cat_item_id = (transaction % 5) + 1
            okay("Creating New Transaction, #", transaction)
            Transaction.add(
                session=session,
                name=f"Test Source: {transaction}",
                transaction_date=random_date.strftime("%m/%d/%y"),
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
                statement = select(Transaction).where(
                    Transaction.category_item_id == category_item.id,
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                )
                result = session.exec(statement)
                transactions = result.all()
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
    :return: A Category object with its related data.
    """
    with session:
        # Get the category with the given id
        category = session.get(Category, category_id)
        # Access the categories relationship attribute to get the related category items
        category_items = category.category_items
        for category_item in category_items:
            # Access the transactions relationship attribute to get the related transactions
            statement = select(Transaction).where(
                Transaction.category_item_id == category_item.id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
            )
            result = session.exec(statement)
            transactions = result.all()
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
        # Access the transactions relationship attribute to get the related trnasactions
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

    with session:
        # Access the transactions relationship attribute to get the related transactions
        statement = select(Transaction).where(
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
        )
        result = session.exec(statement)
        transactions = result.all()
        return transactions


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
        transaction.updated = datetime.utcnow()

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

        new_item = CategoryItem.add(
            session=session,
            name=name,
            budgeted=budgeted_amount,
            category_id=category.id,
        )
        session.commit()
        session.refresh(new_item)


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
        category_item.updated = datetime.utcnow()

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
    category_item_name: str,
) -> None:
    """Function to save transaction to the database

    Args:
        name (ui.input): string name of the transaction
        transaction_date (ui.input): string representation of when the transaction occured
        category_item_name (ui.select): name of the category item that the transaction is under
        amount (ui.number): ztring representation of the dollar amount of the transaction
    """

    with session:
        category_item: CategoryItem = session.exec(
            select(CategoryItem).where(CategoryItem.name == category_item_name)
        ).first()

        transaction = Transaction(
            name=name,
            transaction_date=transaction_date,
            category_item_id=category_item.id,
            amount=amount,
        )
        session.add(transaction)
        print("Saving Transaction")
        session.commit()
        print("Transaction Saved")
        session.refresh(transaction)
        print(transaction)


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
