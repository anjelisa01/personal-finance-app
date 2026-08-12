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

class Category(Base):
    __tablename__="category"

    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    category_name:Mapped[str]

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
    