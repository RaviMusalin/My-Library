"""CRUD operations."""

from model import db, User, Book, Rating, Owned, connect_to_db


def create_user(username, email, password, type_of_user="user"):
    """Create and return a new user."""

    user = User(user_name=username, email=email, password=password, type_of_user=type_of_user)

    return user


def create_book(title, author, isbn=None, book_cover=None):
    """Create and return a new book."""

    book = Book(
        title=title,
        author=author,
        isbn=isbn,
        book_cover=book_cover 
    )

    return book


def get_books():
    """Get all books and return"""

    return Book.query.all()


def get_users_library(user_id):

    user = get_user_by_id(user_id)
    
    if user: 
        return user.users_library
    else:
        return []
    

def create_rating(user, book, score, body):
    """Create and return a new rating."""

    rating = Rating(user=user, books=book, score=score, body=body)

    return rating


def book_details_by_id(book_id):
    """Gets a book by it's book id"""

    return Book.query.get(book_id)


def user_details():
    """Gets all users"""

    return User.query.all()


def get_user_by_id(user_id):
    """Gets the details of a specific user"""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Gets a user by checking to see if the email exists"""
   
    return User.query.filter(User.email == email).first()


def get_user_by_username(username):
    """Get user by username"""
    
    return User.query.filter(User.user_name == username).first()


def get_book_by_isbn(isbn):
    """Get book by isbn"""

    return Book.query.filter(Book.isbn == isbn).first()


def get_total_ratings(book_id):
    """Get how many ratings there are for a book"""
    
    return Rating.query.filter(Rating.book_id == book_id).count()


def ratings_by_id(book_id):

    return Rating.query.filter(Rating.book_id == book_id).all()


def average_rating(book_id):
    """Calculates the average rating score"""
    num_total_ratings = get_total_ratings(book_id)
    if num_total_ratings == 0:
        return "No ratings yet"

    rating_sum = 0
    all_ratings = ratings_by_id(book_id)
    
    for rating in all_ratings:
        rating_sum += rating.score
    
    avg_rating = round(rating_sum / num_total_ratings, 2)

    return avg_rating



if __name__ == "__main__":
    from server import app

    connect_to_db(app)
