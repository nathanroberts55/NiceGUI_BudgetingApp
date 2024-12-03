from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Session, Field, Relationship
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
    from category_model import Category


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = None
    created: datetime = Field(default=datetime.now(timezone.utc))
    updated: datetime = Field(default=datetime.now(timezone.utc))

    # Relationship to Category
    categories: Optional[List["Category"]] = Relationship(
        back_populates="",
    )

    @property
    def budgeted_total(self) -> float:
        return sum(category.budgeted_total for category in self.categories)

    @property
    def actual_total(self) -> float:
        return sum(category.actual_total for category in self.categories)

    @property
    def budgeted_balance(self) -> float:
        total_in = sum(
            category.budgeted_total
            for category in self.categories
            if category.name == "Income"
        )
        total_out = sum(
            category.budgeted_total
            for category in self.categories
            if category.name != "Income"
        )
        return total_in - total_out

    @property
    def actual_balance(self) -> float:
        total_in = sum(
            category.actual_total
            for category in self.categories
            if category.name == "Income"
        )
        total_out = sum(
            category.actual_total
            for category in self.categories
            if category.name != "Income"
        )
        return total_in - total_out

    @property
    def actual_total_out(self) -> float:
        total_out = sum(
            category.actual_total
            for category in self.categories
            if category.name != "Income"
        )
        return total_out

    @property
    def actual_total_in(self) -> float:
        total_in = sum(
            category.actual_total
            for category in self.categories
            if category.name == "Income"
        )
        return total_in

    @property
    def budgeted_total_out(self) -> float:
        total_out = sum(
            category.budgeted_total
            for category in self.categories
            if category.name != "Income"
        )
        return total_out

    @property
    def budgeted_total_in(self) -> float:
        total_in = sum(
            category.budgeted_total
            for category in self.categories
            if category.name == "Income"
        )
        return total_in

    # Define a class method to add the new object to the session
    @classmethod
    def add(cls, session: Session, **kwargs) -> None:
        with session:
            budget = cls(**kwargs)
            session.add(budget)
            return budget

    @classmethod
    def create(cls, session: Session, **kwargs) -> "Budget":
        with session:
            budget = cls(**kwargs)
            session.add(budget)
            session.commit()
            session.refresh(budget)
            return budget
