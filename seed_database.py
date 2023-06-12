"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb booksdb')
os.system('createdb booksdb')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/books.json') as f:
    book_data = json.loads(f.read())
    print(book_data)

# Create books, store them in list so we can use them
# to create fake ratings later
books_in_db = []
for book in book_data:
    title, author = (
        book["title"],
        book["author"]
    )

    db_book = crud.create_book(title, author)
    books_in_db.append(db_book)

model.db.session.add_all(books_in_db)
model.db.session.commit()


for n in range(10):
    email = f"user{n}@test.com"  
    password = "test"
    username = f"{n}user" 

    user = crud.create_user(username, email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_book = choice(books_in_db)
        score = randint(1, 5)
        body = "This is a test body text" 

        rating = crud.create_rating(user, random_book, score, body)
        model.db.session.add(rating)

model.db.session.commit()