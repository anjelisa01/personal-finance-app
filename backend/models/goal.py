#imports
from sqlalchemy import ForeignKey,String
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column

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
    target_amount:Mapped[float]
    saved_amount:Mapped[float]
    due_date:Mapped[datetime]

    #fk
    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id") #
    )
    
    #relationship
    user:Mapped["User"]=relationship(
        back_populates="goals" 
    )