from typing import Optional, List
from datetime import datetime
from sqlmodel import Column, SQLModel, Session, Field, Relationship, String


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = None

    # Relationship to Category
    categories: Optional[List["Category"]] = Relationship(back_populates="")

    @property
    def budgeted_total(self) -> float:
        return sum(category.budgeted_total for category in self.categories)

    @property
    def actual_total(self) -> float:
        return sum(category.actual_total for category in self.categories)

    @property
    def balance(self) -> float:
        return self.budgeted_total - self.actual_total

    # Define a class method to add the new object to the session
    @classmethod
    def add(cls, session: Session, **kwargs) -> None:
        budget = cls(**kwargs)
        session.add(budget)
        return budget


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = None

    # Relationship to Budget
    budget_id: Optional[int] = Field(default=None, foreign_key="budget.id")
    budget: Optional[Budget] = Relationship(back_populates="categories")

    # Relationship to Category Item
    category_items: Optional[List["CategoryItem"]] = Relationship(
        back_populates="category"
    )

    # Calculated Columns
    @property
    def budgeted_total(self) -> float:
        # The budgeted_total property calculates the sum of the budgeted_total values of all related CategoryItem objects
        return sum(category_item.budgeted for category_item in self.category_items)

    @property
    def actual_total(self) -> float:
        # The actual_total property calculates the sum of the actual_total values of all related CategoryItem objects
        return sum(category_item.actual for category_item in self.category_items)

    @property
    def percent_of_budget(self) -> float:
        # The percent_of_budget property calculates the percentage of actual_total relative to budgeted_total
        if self.budgeted_total:
            return (self.actual_total / self.budgeted_total) * 100
        else:
            return 0.0

    @property
    def over_under(self) -> float:
        # The over_under property calculates the difference between actual_total and budgeted_total
        return self.actual_total - self.budgeted_total

    # Define a class method to save the new object to the database
    @classmethod
    def add(cls, session: Session, **kwargs) -> "Category":
        category = cls(**kwargs)
        session.add(category)
        return category


# region Future Feature
class DebtCategory(Category):
    interest_rate: float = None
    beginning_balance: float = None
    ending_balance: float = None


class SavingCategory(Category):
    interest_rate: float = None
    beginning_balance: float = None
    ending_balance: float = None


# endregion Future Feature


class CategoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default=datetime.utcnow())
    updated: datetime = Field(default=datetime.utcnow())
    name: str = None
    budgeted: str = "0.00"
    over_under: float = None

    # Relationship to Category
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="category_items")
    # Relationship to Transaction
    transactions: Optional[List["Transaction"]] = Relationship(
        back_populates="category_item"
    )

    # Calculated Columns
    @property
    def actual(self) -> float:
        # The actual_total property calculates the sum of the actual_total values of all related CategoryItem objects
        return sum(transaction.amount for transaction in self.transactions)

    @property
    def percent_of_budget(self) -> float:
        # The percent_of_budget property calculates the percentage of actual_total relative to budgeted_total
        if self.budgeted:
            return (self.actual / self.budgeted) * 100
        else:
            return 0.0

    @property
    def over_under(self) -> float:
        # The over_under property calculates the difference between actual_total and budgeted_total
        return self.actual - self.budgeted

    # Define a class method to save the new object to the database
    @classmethod
    def add(cls, session: Session, **kwargs) -> "CategoryItem":
        category_item = cls(**kwargs)
        session.add(category_item)
        return category_item


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default=datetime.utcnow())
    updated: datetime = Field(default=datetime.utcnow())
    transaction_date: str = None
    name: str = None
    amount: str = None

    # Relationship to Category Item
    category_item_id: Optional[int] = Field(default=None, foreign_key="categoryitem.id")
    category_item: Optional[CategoryItem] = Relationship(back_populates="transactions")

    # Define a class method to save the new object to the database
    @classmethod
    def add(cls, session: Session, **kwargs) -> "Transaction":
        transaction = cls(**kwargs)
        session.add(transaction)
        return transaction
