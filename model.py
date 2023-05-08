"""Models for Library app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    ratings = db.relationship("Rating", back_populates="user")
    ownedbook = db.relationship("Owned", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username} email={self.email}>"


class Book(db.Model):
    """A Book."""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.Text)
    genre = db.Column(db.Text)
    # Should ISBN be here?

    ratings = db.relationship("Rating", back_populates="books")
    ownedbook = db.relationship("Owned", back_populates="books")

    def __repr__(self):
        return f"<Movie movie_id={self.book_id} title={self.title} author={self.author}>"


class Rating(db.Model):
    """A book rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    books = db.relationship("Book", back_populates="ratings")
    user = db.relationship("User", back_populates="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"
    
class Owned(db.Model):
    """A table of the books a user owns"""

    __tablename__ = 'ownedbooks'

    owned_books_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    books = db.relationship("Book", back_populates="ownedbook")
    user = db.relationship("User", back_populates="ownedbook")

    def __repr__(self):
        return f"<Owned owned_books_id={self.owned_books_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///booksdb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)