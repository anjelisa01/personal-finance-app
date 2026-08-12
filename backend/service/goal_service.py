#import
from sqlalchemy.orm import Session
from sqlalchemy import select

#model and schema
from models.goal import Goal
from schemas.goal import GoalBase,GoalUpdate

#util
from core.logger import logger
from core.exceptions import ResourceNotFoundError,ResourceExistedError

def get_goal_name(db:Session,user_id:int,goal_name:str):
    stmt=select(Goal).where(
        Goal.user_id==user_id,
        Goal.goal_name==goal_name)
    return db.scalars(stmt).first()

class GoalService:
    def __init__(self,db: Session,user_id:int):
        self.db = db
        self.user_id=user_id
        
    def create(self,payload:GoalBase):
        existing=get_goal_name(self.db,self.user_id,payload.goal_name)
        if existing:
            raise ResourceExistedError("Goal",payload.goal_name)

        #build goal data
        goal=Goal(**payload.model_dump())
        #no duplcate checking, up to user sometimes the goals are the sama over and over again        
        goal.user_id=self.user_id
        #insert
        try:
            self.db.add(goal)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 
        logger.info("Goal created, goal id=%s", goal.id) 
        self.db.refresh(goal)
        return goal

    def read_one(self,goal_id:int):
        goal=self.db.scalar(
        select(Goal).where(
            Goal.user_id==self.user_id,
            Goal.id==goal_id)
        )
        #check if goal is none
        #if the return value of goal is None, then:
        if goal is None:
            raise ResourceNotFoundError("Goal", goal_id)
        return goal
       
    def read_all(self):
        return self.db.scalars(
            select(Goal).where(Goal.user_id == self.user_id)
        ).all()
        
    def update(self,goal_id:int,payload:GoalUpdate):
        goal=self.db.scalar(
            select(Goal).where(
                Goal.user_id==self.user_id,
                Goal.id==goal_id))
        if goal is None:
            raise ResourceNotFoundError("Goal", goal_id)
        #build update data
        update_data=payload.model_dump(exclude_unset=True)

        #if goal_name existed in database
        if "goal_name" in update_data:
            existing=get_goal_name(self.db,self.user_id,update_data["goal_name"])
            if existing:
                raise ResourceExistedError("Account",update_data["goal_name"])
        #update
        try:
            for field,value in update_data.items():
                setattr(goal,field,value)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Goal updated, goal id =%s", goal_id)
        self.db.refresh(goal)
        return goal

    def delete(self,goal_id:int):
        goal=self.db.scalar(
            select(Goal).where(
                Goal.user_id==self.user_id,
                Goal.id==goal_id))
        if goal is None:
            raise ResourceNotFoundError("Goal", goal_id)
        #delete
        try:
            self.db.delete(goal)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Goal deleted,  goal id=%s", goal_id) 
        return{"message":"deleted"}
