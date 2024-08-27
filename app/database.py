from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import setting
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Connection for SQLALCHEMY 
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




## FOR REFERNCE!!!! NOT USE
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# # Connection To DB
# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fasiapi' , user = 'postgres', password = '12345', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("\nConnection to Database was succesfull..\n")
#         break
#     except Exception as e:
#         print("There something wrong connect to Database")
#         print("Error: ", e)
#         time.sleep(2)