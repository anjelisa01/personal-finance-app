#imports
from sqlalchemy import ForeignKey,func,String
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.database import Base

'''
INFORMATION:
user is independent, doesnt have any fk
user-categories: one to many
user-accounts: one to many
user-goals: one to many
'''

class User(Base):
    __tablename__="users"

    #fields
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(255))
    email:Mapped[str]=mapped_column(String(255))
    currency:Mapped[str]=mapped_column(String(255))
    hashed_password:Mapped[str]=mapped_column(String(255))
    deleted_at:Mapped[datetime]=mapped_column(
        nullable=True
    )
    created_at:Mapped[datetime]=mapped_column(
        server_default=func.now() #this is fill created_at at the database level
    )

    #relationship
    categories: Mapped[list["Category"]]=relationship(
        back_populates="user")
    accounts: Mapped[list["Account"]]=relationship(
        back_populates="user")
    goals: Mapped[list["Goal"]]=relationship(
        back_populates="user")


'''
if making changes in the sqlalchemy models level, i have to also change on the posgresql level
changing in sqlalchemyy level doesnt automatically change the db 

Because SQLAlchemy is NOT an ORM that syncs schema automatically 
(unless you explicitly use migration tools or drop/create tables).
....
so back_populates needed both table that connected to defined that they are conncted 

'''