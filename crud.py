"""CRUD operations."""

from model import db, User, Book, Rating, Owned, connect_to_db


def create_user(username, email, password, type_of_user="user"):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password, type_of_user=type_of_user)

    return user


def create_book(title, author, genre, isbn=None, book_cover=None):
    """Create and return a new book."""

    book = Book(
        title=title,
        author=author,
        genre=genre,
        isbn=isbn,
        book_cover=book_cover # Book cover from API?
    )

    return book


def get_books():
    """Get all books and return"""

    return Book.query.all()


def create_rating(user, book, score, body):
    """Create and return a new rating."""

    rating = Rating(user=user, books=book, score=score, body=body)

    return rating

def create_book_owned(user, book):
    # What to put in a function to create books owned for a specific user?
    owned_book = Owned(user=user, books=book)

    return owned_book

def book_details_by_id(book_id):

    return Book.query.all(book_id)

def user_details():

    return User.query.all()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
