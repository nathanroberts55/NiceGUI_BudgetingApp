from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Session, Column, Integer, ForeignKey, Field, Relationship
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlite3 import Connection as SQLite3Connection


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


if TYPE_CHECKING:
    from .category_model import Category
    from .transactions_model import Transaction


class CategoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default=datetime.now(timezone.utc))
    updated: datetime = Field(default=datetime.now(timezone.utc))
    name: str = None
    budgeted: str = "0.00"
    over_under: float = None

    # Relationship to Category
    category_id: Optional[int] = Field(
        default=None,
        foreign_key="category.id",
        sa_column=Column(Integer, ForeignKey("category.id", ondelete="CASCADE")),
    )
    category: Optional["Category"] = Relationship(
        back_populates="category_items",
    )
    # Relationship to Transaction
    transactions: Optional[List["Transaction"]] = Relationship(
        back_populates="category_item",
        sa_relationship_kwargs={"cascade": "all"},
    )

    # Calculated Columns
    @property
    def actual(self) -> float:
        # The actual_total property calculates the sum of the actual_total values of all related CategoryItem objects
        return sum(float(transaction.amount) for transaction in self.transactions)

    @property
    def percent_of_budget(self) -> float:
        # The percent_of_budget property calculates the percentage of actual_total relative to budgeted_total
        if float(self.budgeted):
            return (float(self.actual) / float(self.budgeted)) * 100
        else:
            return 0.0

    @property
    def over_under(self) -> float:
        # The over_under property calculates the difference between actual_total and budgeted_total
        return float(self.actual) - float(self.budgeted)

    # Define a class method to save the new object to the database
    @classmethod
    def create(cls, session: Session, **kwargs) -> "CategoryItem":
        with session:
            category_item = cls(**kwargs)
            session.add(category_item)
            session.commit()
            session.refresh(category_item)
            return category_item
