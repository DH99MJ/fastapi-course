from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends # For SQLALCHEMY 
from ..database import get_db
from sqlalchemy.orm import Session

# Make a @router instead of @router

router = APIRouter(
    prefix = "/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    # hash password
    hased_password = utils.hash(user.password)
    user.password  = hased_password 

    # Keep other same
    current_user = models.User(**user.dict())

    # Check if existing user 
    check_user_duplicate = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user_duplicate:
       raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="The email or password it already existing in our database..."
    )

    # Send into db
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()
    return users

@router.get("/{id}",status_code=200, response_model=schemas.UserOut)
def  get_user(id: int , db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(
            status_code=404,
            detail=f"The id: {id} you provided not found in our database."
        )
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    # Search the user ID and comparing with ID we gonna providing then DELETING
    search_user = db.query(models.User).filter(models.User.id == id)

    # if not exist
    if search_user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The id: {id} you provided not found in our database."
        )

    # if exist
    search_user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)

@router.put("/{id}", response_model=schemas.UserCreate)
def update_user(id: int , updated_user: schemas.UserCreate ,db: Session = Depends(get_db)):
    
    # Find the id which we entered and comparing from db
    update_query = db.query(models.User).filter(models.User.id == id) 
    user_delete = update_query.first()

    # if not exist
    if user_delete == None:
        raise HTTPException(
            status_code=404,
            detail=f"The id: {id} you provided not found in our database."
        )

    # if exist
    update_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()
    