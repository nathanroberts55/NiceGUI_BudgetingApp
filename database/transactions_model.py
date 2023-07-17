from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Session, Field, Relationship

if TYPE_CHECKING:
    from .catergory_items_model import CategoryItem


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default=datetime.utcnow())
    updated: datetime = Field(default=datetime.utcnow())
    transaction_date: str = None
    name: str = None
    amount: str = None

    # Relationship to Category Item
    category_item_id: Optional[int] = Field(default=None, foreign_key="categoryitem.id")
    category_item: Optional["CategoryItem"] = Relationship(
        back_populates="transactions"
    )

    # Define a class method to save the new object to the database
    @classmethod
    def add(cls, session: Session, **kwargs) -> "Transaction":
        transaction = cls(**kwargs)
        session.add(transaction)
        return transaction
