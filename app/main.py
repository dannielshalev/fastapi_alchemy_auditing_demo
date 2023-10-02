from fastapi import FastAPI, HTTPException, Depends
from fastapi import Response
from fastapi.requests import Request
from pydantic import BaseModel, Field
from app import models
from app.database import engine, session_local
from sqlalchemy.orm import Session


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db(request: Request):
    return request.state.db


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = session_local()
        response = await call_next(request)
        response_body = b''
        if all(filter not in request.url.__str__() for filter in ['docs', 'openapi.json', 'favicon.ico']):
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(content=response_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type)
            await store_audit_middleware(request, response_body, request.state.db)
    finally:
        request.state.db.close()
    return response


async def store_audit_middleware(request: Request, response_body, db):
    audit_entry = models.Audit()
    audit_entry.url = request.url.__str__()
    audit_entry.headers = request.headers.items()
    audit_entry.method = request.method
    audit_entry.response = response_body.decode()
    db.add(audit_entry)
    db.commit()
    return audit_entry


@app.get("/")
async def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()


@app.post("/book")
async def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
