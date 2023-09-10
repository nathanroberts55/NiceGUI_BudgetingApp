from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Session, Integer, Column, ForeignKey, Field, Relationship
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
    from .catergory_items_model import CategoryItem


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created: datetime = Field(default=datetime.utcnow())
    updated: datetime = Field(default=datetime.utcnow())
    transaction_date: str = None
    name: str = None
    amount: str = None

    # Relationship to Category Item
    category_item_id: Optional[int] = Field(
        default=None,
        foreign_key="categoryitem.id",
        sa_column=Column(Integer, ForeignKey("categoryitem.id", ondelete="CASCADE")),
    )
    category_item: Optional["CategoryItem"] = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs={"cascade": "all, delete"},
    )

    # Define a class method to save the new object to the database
    @classmethod
    def add(cls, session: Session, **kwargs) -> "Transaction":
        transaction = cls(**kwargs)
        session.add(transaction)
        return transaction
