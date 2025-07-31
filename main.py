import base64
from datetime import datetime
from email.header import Header
from http.client import HTTPException

from cloudinit.reporting.events import status
from fastapi import FastAPI, Request
from typing import Optional, List
from pydantic import  BaseModel

from starlette.responses import Response, JSONResponse, HTMLResponse

app = FastAPI()

@app.get("/ping")
def ping():
    return Response(content="pong",status_code=200)
@app.get('/home')
def hello():
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return HTMLResponse(content="<h1>404 NOT FOUND</h1>", status_code=404)
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime


posts_db: List[Post] = []


@app.post("/posts", status_code=201)
def create_posts(new_posts: List[Post]):
    posts_db.extend(new_posts)
    return posts_db

@app.get("/posts")
def get_posts():
    return posts_db


@app.put("/posts")
def put_posts(new_posts: List[Post]):
    for new_post in new_posts:
        for i, existing_post in enumerate(posts_db):
            if existing_post.title == new_post.title:
                if existing_post != new_post:
                    posts_db[i] = new_post

        else:
            posts_db.append(new_post)

    return {

        "posts": posts_db
    }


