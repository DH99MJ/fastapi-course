from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# Create Class Post <name it doesn't matter>
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Optional field.. quz we assign boolean "True"


class PostCreate(PostBase): # PostCreate extend PostBase 'Like java'
    pass



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

                      # Post -> PostOut
class Post(PostBase): # Post extend PostBase , # Respone for user 'NO NEED TO DISPLAY Created at and ID' so this important
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:        # IMPORTANT: Bquz it will convert pydantic into python dict
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    total_Vote: int # Label for join database
    
    class Config:        # IMPORTANT: Bquz it will convert pydantic into python dict
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # 1 it means liked! 0 it means remove like
                      # and 'conint' means only takes number 1 and less..