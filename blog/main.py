from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schema import Blog, ShowBlog, User, ShowUser
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from passlib.context import CryptContext

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)
#Blog Start
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
def destroy(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ShowBlog, tags=["Blog"])
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    else:
        blog.update({'title': request.title})
        db.commit()
        return {'Updated Successfully'}

@app.get('/blog', response_model=List[ShowBlog], tags=["Blog"])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=["Blog"])
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not available')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'detail': f'Blog with the id {id} not available'}
    return blog

#Blog Ends

#User Starts

pwd_cxt = CryptContext(schemes =['bcrypt'], deprecated = "auto")

@app.post('/user', response_model=ShowUser, tags=["User"])
def create_user(request: User, db: Session = Depends(get_db)):
    hashed_pass = pwd_cxt.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=ShowUser, tags=["User"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user