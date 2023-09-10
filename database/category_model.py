from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Session, Field, Relationship

# For Cascading Deletes | https://github.com/tiangolo/sqlmodel/issues/213

if TYPE_CHECKING:
    from .budget_model import Budget
    from .catergory_items_model import CategoryItem


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = None

    # Relationship to Budget
    budget_id: Optional[int] = Field(default=None, foreign_key="budget.id")
    budget: Optional["Budget"] = Relationship(back_populates="categories")

    # Relationship to Category Item
    category_items: Optional[List["CategoryItem"]] = Relationship(
        back_populates="category"
    )

    # Calculated Columns
    @property
    def budgeted_total(self) -> float:
        # The budgeted_total property calculates the sum of the budgeted_total values of all related CategoryItem objects
        return sum(
            float(category_item.budgeted) for category_item in self.category_items
        )

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
        with session:
            category = cls(**kwargs)
            session.add(category)
            return category

    # Define a class method to save the new object to the database
    @classmethod
    def create(cls, session: Session, **kwargs) -> "Category":
        with session:
            category = cls(**kwargs)
            session.add(category)
            session.commit()
            session.refresh(category)
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
