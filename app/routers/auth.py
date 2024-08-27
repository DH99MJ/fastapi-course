from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):

                                        # DataBase      # ==        # login page 
    user = db.query(models.User).filter(models.User.email ==  user_credentials.username).first()
    # if not exist
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
                    # Verify 
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # Create a token
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    # return
    return {"token": access_token, "token_type": "bearer"}
