from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name': 'Gagan'}}

@app.get('/about')
def index():
    return {'data': 'about page'}

@app.get('/blog')
def index(limit = 10, published: bool = True, sort: Optional[str]= None):
    return {'blog': 'all unpublished blogs'}

@app.get('/blog/unpublished')
def unpublished():
    return {'blog': 'all unpublished blogs'}

@app.get('/blog/{id}')
def index(id: int):
    return {'blog': id}

@app.get('/blog/{id}/comments')
def index(id: int):
    return {'blog': {'1', '2'}}

class Blog(BaseModel): #Model Creation
    title: str
    body: str
    published: Optional[bool]

#Model based work
@app.post('/blog')
def create_blog(request: Blog):
    return {'data': request}