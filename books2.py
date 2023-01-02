from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        title="Description of the book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4962-b3fc-2c963f66afa6", "title": "title 6",
                "author": "author 6", "description": "description 6", "rating": 66
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(
        None, title="Description of the book", max_length=100, min_length=1)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message": f"Hey, why do you want {exception.books_to_return} books? You need to read more!"})


# @app.post("/books/login")
# async def book_login(username: str = Form(), password: str = Form()):
#     return {"username": username, "password": password}


@app.post("/books/login/")
async def book_login(book_id: UUID, username: str = Header(None), password: str = Header(None)):
    if username == "FastAPIUser" and password == "test1234!":
        for x in BOOKS:
            if x.id == book_id:
                return x
        raise raise_item_cannot_be_found_exception()
    else:
        return {"message": "Invalid User"}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        if x.id == book_id:
            BOOKS[counter] = book
            return BOOKS[counter]
        counter += 1
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        if x.id == book_id:
            del BOOKS[counter]
            return f'ID: {book_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="title 1",
                  author="author 1", description="description 1", rating=61)
    book_2 = Book(id="3fa85f64-5727-4562-b3fc-2c963f66afa6", title="title 2",
                  author="author 2", description="description 2", rating=62)
    book_3 = Book(id="3fa85f64-5737-4562-b3fc-2c963f66afa6", title="title 3",
                  author="author 3", description="description 3", rating=63)
    book_4 = Book(id="3fa85f64-5747-4562-b3fc-2c963f66afa6", title="title 4",
                  author="author 4", description="description 4", rating=64)
    book_5 = Book(id="3fa85f64-5757-4562-b3fc-2c963f66afa6", title="title 5",
                  author="author 5", description="description 5", rating=65)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found", headers={
        "X-Header-Error": "Nothing to be seen at the UUID"
    })
