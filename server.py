"""Server for library  app."""
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
import requests
import os 

# Helper function to put keyword in params 
def get_API_data(keyword):
    """Helper function to put keyword in params """
    API_KEY = os.environ["GOOGLE_KEY"]

    payload = {'q': {keyword}, 'key': API_KEY}
    res = requests.get('https://www.googleapis.com/books/v1/volumes?', params=payload)

    book_data = res.json()
    book_results = book_data['items']
    print("Hello", len(book_results))
    return book_results


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
    avg_ratings = crud.average_rating(book_id)
    print(avg_ratings)
    return render_template("book_details.html", book=book, avg_ratings=avg_ratings)


# FIX THIS ROUTE
# @app.route('/books/<book_id>')
# def book_ratings(book_id):
#     # Get all the ratings 
#     book = crud.book_details_by_id(book_id)
#     ratings = crud.get_book_ratings(book_id)

#     return render_template("book_details.html", book=book, ratings=ratings)

@app.route('/users/<user_id>')
def get_user_details(user_id):
    """Show individual User details"""

    user = crud.get_user_by_id(user_id)

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

    return redirect("/users")

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


@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    
    return render_template('homepage.html')


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
    score = request.form.get("score")
    body = request.form.get("review")
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    book_id = request.form.get("book_id")
    book = crud.book_details_by_id(book_id)

    
    new_rating = crud.create_rating(user, book, score, body)
    db.session.add(new_rating)
    db.session.commit()

    book.ratings.append(new_rating)
    db.session.commit()
    avg_ratings = crud.average_rating(book_id)

    return render_template('book_details.html', book=book, avg_ratings=avg_ratings)


@app.route('/search')
def book_search():
    """Search for a book"""
    
    return render_template("search.html")


@app.route('/search/results')
def book_search_results():
    """Get's result of book search"""
    keyword = request.args.get("search_keyword")
    
    books = get_API_data(keyword)
    
    books_isbn = []
    
    for book in books:
        if 'industryIdentifiers' in book['volumeInfo']:
            books_isbn.append(book['volumeInfo']['industryIdentifiers'][0]['identifier'])
        # books_isbn = [book['volumeInfo']['industryIdentifiers'][0]['identifier'] for book in books]

    if "user_id" in session:
        user_id = session["user_id"]
        user = crud.get_user_by_id(user_id)
        user_library = crud.get_users_library(user_id)
    
    user_isbns = [x.isbn for x in user_library]   

    filtered_books = [x for x in user_isbns if x in books_isbn] 
# https://stackoverflow.com/questions/34288403/how-to-keep-elements-of-a-list-based-on-another-list
# https://stackoverflow.com/questions/28644951/django-how-to-apply-conditional-attribute-to-html-element-in-template
    return render_template("search_results.html", books=books, user=user, user_isbns=user_isbns, books_isbn=books_isbn, filtered_books=filtered_books)

@app.route('/saved_to_own', methods=["POST"])
def save_book_to_owned():
    """Get book from API and add to table"""

    title = request.json.get("title")
    author = request.json.get("author")
    isbn = request.json.get("isbn")
    book_cover = request.json.get("book_cover")
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)

    if not crud.get_book_by_isbn(isbn):
        new_book = crud.create_book(title, author, isbn, book_cover)
        db.session.add(new_book)
        db.session.commit()
    else:
        new_book = crud.get_book_by_isbn(isbn)

    user.users_library.append(new_book)
    db.session.commit()

    return "book saved"

@app.route('/return')
def go_back():
    return redirect('/')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)