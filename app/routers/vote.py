from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from typing import List, Optional

router = APIRouter(
    prefix= "/vote",
    tags=["VOTE"] #for FastAPI documentation group
)


@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user:int = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {vote.post_id} doesn't exist.")
        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        print("hi!")
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"msg":"successfully voted!"}

    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Vote doesn't exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"msg": "vote deleted successfully"}
        




