#impors
from sqlalchemy import ForeignKey,func,String,Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from decimal import Decimal

from core.database import Base
'''
INFORMATION:
Budget have fk on user_id
budget - user: many to one
category-budget: one to one
category-transactions: one to many
'''

#enum transaction types
from enum import Enum
from sqlalchemy import Enum as SQLEnum
class Period(str,Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY="monthly"

class Budget(Base):
    __tablename__="budget"

    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    amount:Mapped[Decimal]=mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00")
    )
    period:Mapped[Period] = mapped_column(
        SQLEnum(
            Period,
            name="period",
            native_enum=True,
            create_type=False,
            values_callable=lambda e: [item.value for item in e],
        ),
        nullable=False)
    
    #fk
    category_id:Mapped[int]=mapped_column(
        ForeignKey("category.id"), 
        unique=True 
    )

    #relationship
    category:Mapped["Category"]=relationship(
        back_populates="budget" 
    )