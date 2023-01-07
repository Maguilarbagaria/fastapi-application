from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix= "/posts",
    tags=["POSTS"] #for FastAPI documentation group
)


@router.get("/",response_model= List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit:int = 10, skip = 0, search: Optional[str]= ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(
            limit).offset(skip).all()


    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#WITH SQL# def create_post(post: Post, ):
    # cursor.execute("""INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING * """, 
    #     (post.title, post.content, post.publish)) #never in f strings {to avoid sql injections}
    # new_post = cursor.fetchone()
    # conn.commit() #saving changes in postgres
#WITH ORM#

    new_post =models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post) #adding to db
    db.commit()      #saving changes
    db.refresh(new_post) #refreshing

    return new_post


@router.get("/{id}", response_model= list[schemas.PostOut])
def get_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

#WITH SQL# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#     post = cursor.fetchone()
#     print(id)

#WITH ORM#

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail= f'post with id:{id} was not found.')
    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return{post}


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
#     post = cursor.fetchone()
#     conn.commit()
#WITH ORM#
def delete_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f'Post with id: {id} was not found.')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_query.delete(synchronize_session=False)
    db.commit()
    return(Response(status_code=status.HTTP_204_NO_CONTENT))



@router.put("/{id}")
# def update_post(id:int, post: Post):   
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, publish = %s WHERE id = %s RETURNING * """, 
#                     (post.title, post.content, post.publish, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#WITH ORM#
def update_post(id:int, upd_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail= f'Post with id: {id} was not found.')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


    post_query.update(upd_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()