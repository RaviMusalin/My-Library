"""Server for library  app."""
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
import requests
import os 

API_KEY = os.environ["GOOGLE_KEY"]

payload = {'q': 'The+lion+the+witch+and+the+wardrobe', 'key': API_KEY}

res = requests.get('https://www.googleapis.com/books/v1/volumes?', params=payload)

book_data = res.json()

book_results = book_data['items']

for book in book_results:
    title = book['volumeInfo']['title']
    author = book['volumeInfo']['authors']
    description = book['volumeInfo']['description']
    print(f'Title of book: {title}')
    print(f'Written by: {author}')
    print(f'{description}')
# for book in book_results:
#     print(book)

# for i in range(book_results):
#     book_title = book_data['items'][i].get('kind')
#     author = book_data['items'][i].get('id')
#     print(f'{book_title}: {author}')






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
    """Shows a list of all books"""

    books = crud.get_books()

    return render_template("all_books.html", books=books) # QUESTION: Why is book = books? What does declaring this do?


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
    """Shows a list of all users"""

    users = crud.user_details()

    return render_template("users.html", users=users)


@app.route('/users', methods=["POST"]) # Why are we allowed two users routes?: Any issues with this?
def register_user():
    """Create a new user."""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("An account with this email already exists")
    else:  
        user = crud.create_user(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")
#  REFER BACK TO API LECTURE


@app.route('/login', methods=["POST"])
def user_login():
    """User login"""

    username = request.form.get("username")
    # email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_username(username)

    if not user or user.password != password:
        flash("Please check your login credentials")
        return redirect('/')
            
    else:# Log in user by storing the user's username in session
        session["user_id"] = user.user_id
        flash(f"Welcome back, {user.user_name}!")    
        
        return redirect('/user_details')

@app.route('/user_details')
def user_library():

    if "user_id" in session:
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)
        user_library = crud.get_users_library(user_id)

        print(user_library)

        return render_template("user_details.html", user = user, user_library = user_library)# Does logging in save to local DB?
    
    else:
        flash("Please log in") 
        return redirect('/')

@app.route('/rate_book', methods=["POST"])
def book_rating():
    # FINISH FUNCTION TO ADD RATING TO DATABASE
    return render_template("book_details.html")

# @app.route()




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)