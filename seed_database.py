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
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime

    # TODO: create a movie here and append it to movies_in_db