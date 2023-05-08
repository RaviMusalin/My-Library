"""CRUD operations."""

from model import db, User, Book, Rating, Owned, connect_to_db


def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password)

    return user


def create_book(title, author, genre):
    """Create and return a new book."""

    book = Book(
        title=title,
        author=author,
        genre=genre,
        # poster_path=poster_path, Book cover from API?
    )

    return book


def create_rating(user, book, score):
    """Create and return a new rating."""

    rating = Rating(user=user, book=book, score=score)

    return rating

def create_book_owned(user, book):
    
    owned_book = Owned(user=user, book=book)

    return owned_book


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
