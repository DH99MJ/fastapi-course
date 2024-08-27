from passlib.context import CryptContext

# Let's assign bcrypt algorthim for password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

# Create a function call what time you want
def hash(password: str):
    return pwd_context.hash(password)

       # Actual password    # Password from database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)