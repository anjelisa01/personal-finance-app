#imports
from sqlalchemy import ForeignKey,String,Numeric,Date
from datetime import datetime,date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal
from core.database import Base

'''
INFORMATION:
Goal have fk on user_id
goals - user: many to one
'''

class Goal(Base):
    __tablename__="goals"

    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    goal_name:Mapped[str]=mapped_column(String(255))
    target_amount:Mapped[Decimal]=mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00")
    )
    due_date:Mapped[date] = mapped_column(
        Date,
    )

    #fk
    account_id:Mapped[int]=mapped_column(
        ForeignKey("accounts.id"),
        nullable=True,
        default=None    
    )
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
        
    
    #relationship
    account:Mapped["Account"]=relationship(
        back_populates="goals" 
    )
    user:Mapped["User"]=relationship(
            back_populates="goals" 
    )