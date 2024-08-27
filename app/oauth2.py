from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# 1. SECRET KEY 
# 2. ALGORITHM
# 3. EXPIRATION TIME FOR LOGGING OUT


SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    # Logout after 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Corrected: `algorithm` should be a string, not a list
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # Corrected: `algorithms` should be a list containing the algorithm(s)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception 
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    return verify_access_token(token, credentials_exception)
