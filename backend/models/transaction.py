#imports
from sqlalchemy import ForeignKey,String,Numeric,func
from datetime import datetime
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
    created_at:Mapped[datetime]=mapped_column(
        server_default=func.now() #this is fill created_at at the database level
    )

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