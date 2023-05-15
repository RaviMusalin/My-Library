"""Server for library  app."""
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/books')
def all_books():

    books = crud.get_books()

    return render_template("all_books.html", books=books) # QUESTION: Why is book = books?


@app.route('/books/<book_id>')
def book_details(book_id):
    """Show details of book"""

    book = crud.book_details_by_id(book_id)

    return render_template("book_details.html", book=book)

@app.route('/users/<user_id>')
def get_user_details(user_id):
    """Show individual User details"""

    user = crud.user_details_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route('/users')
def all_users():

    users = crud.user_details()

    return render_template("users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

#  REFER BACK TO API LECTURE


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)