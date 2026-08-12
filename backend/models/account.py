#impors
from sqlalchemy import ForeignKey,String,Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal
from core.database import Base
'''
INFORMATION:
Account have fk on user_id
Accounts - user: many to one
Account-transactions: one to many
'''
class Account(Base):
    __tablename__="accounts"
    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    account_name:Mapped[str]=mapped_column(String(255))
    current_balance:Mapped[Decimal]=mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00")
    )
    #fk
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id") #
    )
    #relationship
    user:Mapped["User"]=relationship(
        back_populates="accounts" 
    )
    transactions:Mapped[list["Transaction"]]=relationship(
        back_populates="account" )