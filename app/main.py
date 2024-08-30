from fastapi import FastAPI

from . import models
from .database import engine
# import routers folder
from .routers import post, user, auth,votes
#
from .config import setting

models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

# Create instance for FastAPI
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# IMPORTANT: include_router will access to routers folder then get 'post , user'
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my first API12"}     
