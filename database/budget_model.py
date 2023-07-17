from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Session, Field, Relationship


if TYPE_CHECKING:
    from category_model import Category


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

    # Define a class method to add the new object to the session
    @classmethod
    def add(cls, session: Session, **kwargs) -> None:
        budget = cls(**kwargs)
        session.add(budget)
        return budget
