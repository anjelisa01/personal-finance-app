#imports
from sqlalchemy import ForeignKey,String,Numeric,func,Date,text
from datetime import datetime,date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal

from core.database import Base
'''
INFORMATION:
transaction have fk on account_id 
transaction have fk category_id (optional)
transactions - account: many to one
transactions-category: many to one
'''
#enum transaction types
from enum import Enum
from sqlalchemy import Enum as SQLEnum
class TransactionType(str,Enum):
    EXPENSE = "expense"
    INCOME = "income"
    SAVING="transfer"
class Direction(str,Enum):
    INCOMING="incoming"
    OUTGOING="outgoing"

class Transaction(Base):
    __tablename__="transactions"

    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]
    amount:Mapped[Decimal]=mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00")
    )
    note:Mapped[str]
    transaction_type: Mapped[TransactionType] = mapped_column(
        SQLEnum(
            TransactionType,
            name="transaction_type",
            native_enum=True,
            create_type=False,
            values_callable=lambda e: [item.value for item in e],
        ),
        nullable=False)
    created_at: Mapped[date] = mapped_column(
        Date,
        server_default=text("CURRENT_DATE"),
        nullable=False,
    )
    transfer_id:Mapped[int | None]
    transfer_direction:Mapped[Direction] = mapped_column(
        SQLEnum(
            Direction,
            name="direction",
            native_enum=True,
            create_type=False,
            values_callable=lambda e: [item.value for item in e],
        ),
        nullable=True,
        default=None)

    #fk
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.id"),
        nullable=True,
        default=None
        ) #optional
    account_id:Mapped[int]=mapped_column(
        ForeignKey("accounts.id"),
        nullable=False #mandatory
    )

    #relationship
    account:Mapped["Account"]=relationship(
        back_populates="transactions" 
    )
    category: Mapped["Category | None"] = relationship(
    back_populates="transactions"
    ) 