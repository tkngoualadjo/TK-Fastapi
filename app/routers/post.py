from sqlalchemy import true
from app import oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",  #/id   /posts/{id}
    tags=['Posts']
)


#recuperation des posts dans la base de donnée 

#@router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_post(db: Session= Depends(get_db), current_user: int = Depends (oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
   
    #posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #pour retourner tous les posts
    """ posts =db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() """ #ne retourne que les posts de l'utilisateur qui est connecter

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=true).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return posts


# inserer dans la base de donnée
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session= Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
   
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,   (post.title, post.content, post.published))

    #new_post = cursor.fetchone()
    #conn.commit() pour sauvegarder dans la base de donnée
    #conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#recupérer un post dans la base de donnée
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session= Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id ==id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=true).group_by(models.Post.id).filter(models.Post.id ==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")

    """ if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to perform request action") """
    return post


# supprimer un post dans la base de donnée
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session= Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id)))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id ==id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    
    """ if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to perform request action") """

    post_query.delete(synchronize_session=False)
    db.commit()
   # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# mettre a jour un post dans la base de données
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends (oauth2.get_current_user)):

    #cursor.execute(""" UPDATE  posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #(post.title, post.content, post.published, str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()
    #index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id ==id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")

    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Not authorised to perform request action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()