#impors
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base
'''
INFORMATION:
Category have fk on user_id
categories - user: many to one
category-budget: one to one
category-transactions: one to many
'''

from enum import Enum
from sqlalchemy import Enum as SQLEnum
class CategoryType(str,Enum):
    EXPENSE = "expense"
    INCOME = "income"

class Category(Base):
    __tablename__="category"

    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    category_name:Mapped[str]
    category_type:Mapped[CategoryType] = mapped_column(
        SQLEnum(
            CategoryType,
            name="category_type",
            native_enum=True,
            create_type=False,
            values_callable=lambda e: [item.value for item in e],
        ),
        nullable=False)
    #fk
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id") #
    )

    #relationship
    user:Mapped["User"]=relationship(
        back_populates="categories" 
    )
    budget:Mapped["Budget"]=relationship(
        back_populates="category"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
)
    