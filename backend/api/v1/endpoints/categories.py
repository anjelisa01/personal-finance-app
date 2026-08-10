from fastapi import APIRouter,Depends
from schemas.category import CategoryBase,CategoryResponse

from dependencies.services import get_category_service
from service.category_service import CategoryService

router=APIRouter(tags=["categories"])

@router.post("/",response_model=CategoryResponse)
def add_category(payload:CategoryBase,service:CategoryService=Depends(get_category_service)):
    return service.create(payload)

@router.get("/",response_model=list[CategoryResponse])   
def get_all_categories(service:CategoryService=Depends(get_category_service)):
    return service.read_all()

@router.get("/{category_id}",response_model=CategoryResponse)
def get_one_category(category_id:int,service:CategoryService=Depends(get_category_service)):  
    return service.read_one(category_id)

#Update 
@router.patch("/{category_id}",response_model=CategoryResponse)
def edit_category(category_id:int,payload:CategoryBase,service:CategoryService=Depends(get_category_service)):
    return service.update(category_id,payload)

#delete 
@router.delete("/{category_id}")  
def remove_category(category_id:int,service:CategoryService=Depends(get_category_service)):
    return service.delete(category_id)