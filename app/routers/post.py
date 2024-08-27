from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends # For SQLALCHEMY 
from ..database import get_db
from sqlalchemy.orm import Session




router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 30, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # ---                               # user will able to search based on title
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("total_Vote")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    
    return  posts



#'current_user' We Do this bquz we want from user to login then can create posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # cursor.execute("""INSERT INTO posts (title, content,published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # make_post = cursor.fetchone()
    # conn.commit()

    # ---
    
    new_post = models.Post(owner_id = current_user.id , **post.dict()) # **post_dict() it takes the whole column
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)

    return  new_post

# Get One Posts
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("total_Vote")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    if not post: # If not  existing
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,                               # status code into 404 
                            detail=f"post with this id '{id}' was not found in our database")    # display a message

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    
    # If not found 
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Not found in our database")
    
    print(type(post.owner_id), type(current_user.id))
    # Limit the user to delete own posts ONLY
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s returning *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # print(type(post.owner_id), type(current_user.id))

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found in our database")
    
    # Limit the user to delete own posts ONLY
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to requested action")

    
    # print(type(post.owner_id), type(current_user.id))
    
    post_query.update(updated_post.dict(), synchronize_session=False)   
    db.commit()

    return post_query.first()