#import
from sqlalchemy.orm import Session
from sqlalchemy import select

#models and schemas
from models.user import User
from models.category import Category
from schemas.category import CategoryBase

#utils
from core.logger import logger
from core.exceptions import ResourceExistedError,ResourceNotFoundError

def get_category_name(db:Session,user_id:int,category_name:str):
    stmt=select(Category).where(
        Category.user_id==user_id,
        Category.category_name==category_name)
    return db.scalars(stmt).first()

class CategoryService:
    def __init__(self,db: Session,user_id:int):
        self.db = db
        self.user_id=user_id
    def create(self,payload:CategoryBase):
        #build goal data
        category=Category(**payload.model_dump())
        category.user_id=self.user_id
        
        existing=get_category_name(self.db,self.user_id,payload.category_name)
        if existing:
            raise ResourceExistedError("Category",payload.category_name)
        
        #insert
        try:
            self.db.add(category)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise 
        logger.info("Category created, category id=%s", category.id)
        self.db.refresh(category)
        return category

    def read_one(self,category_id:int):       
        category=self.db.scalar(
        select(Category).where(
            Category.user_id==self.user_id,
            Category.id==category_id)
        )
        if category is None:
            raise ResourceNotFoundError("Category", category_id)
        return category
        
    def read_all(self):
        return self.db.scalars(
            select(Category).where(Category.user_id == self.user_id)
        ).all()
        
    def update(self,category_id:int,payload:CategoryBase):
        category=self.db.scalar(
            select(Category).where(
                Category.user_id==self.user_id,
                Category.id==category_id))
        if category is None:
            raise ResourceNotFoundError("Category", category_id)
        #build update data
        update_data=payload.model_dump(exclude_unset=True)

        #if category_name existed in database
        if "category_name" in update_data:
            existing=get_category_name(self.db,self.user_id,update_data["category_name"])
            if existing:
                raise ResourceExistedError("Category",update_data["category_name"])

        #update
        try:
            for field,value in update_data.items():
                setattr(category,field,value)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Category updated, category id=%s", category_id)
        self.db.refresh(category)
        return category
        
    def delete(self,category_id:int):
        category=self.db.scalar(
            select(Category).where(
                Category.user_id==self.user_id,
                Category.id==category_id))
        if category is None:
            raise ResourceNotFoundError("Category", category_id)
        #delete
        try:
            self.db.delete(category)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        logger.info("Category deleted.  category id=%s", category_id) 
        return{"message":"deleted"}