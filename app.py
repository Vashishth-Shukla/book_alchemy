import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

from data_models import Author, Book, db

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Ensure the 'data' directory exists
db_path = os.path.join(os.getcwd(), "data")
os.makedirs(db_path, exist_ok=True)

# Configure database with an absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f'sqlite:///{os.path.join(db_path, "library.sqlite")}'
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)


@app.route("/")
def home():
    """
    Render the home page showing the list of all books.

    Returns:
        Rendered HTML template for the home page with a list of books.
    """
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Add a new author to the database.

    For GET requests, renders the form for adding an author.
    For POST requests, processes the form data and adds the author to the database.

    Returns:
        Redirects to the authors page on success or re-renders the form on failure.
    """
    if request.method == "POST":
        name = request.form["name"]
        birthdate = request.form.get("birthdate")  # Optional
        date_of_death = request.form.get("date_of_death")  # Optional

        try:
            # Convert dates if provided
            birth_date_obj = (
                datetime.strptime(birthdate, "%Y-%m-%d").date() if birthdate else None
            )
            death_date_obj = (
                datetime.strptime(date_of_death, "%Y-%m-%d").date()
                if date_of_death
                else None
            )

            # Create the Author object
            new_author = Author(
                name=name, birth_date=birth_date_obj, date_of_death=death_date_obj
            )

            # Save to the database
            db.session.add(new_author)
            db.session.commit()
            flash("Author added successfully!", "success")
            return redirect(url_for("authors"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding author: {str(e)}", "danger")
            return redirect(url_for("add_author"))

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Add a new book to the database.

    For GET requests, renders the form for adding a book.
    For POST requests, processes the form data and adds the book to the database.

    Returns:
        Redirects to the home page on success or re-renders the form on failure.
    """
    if request.method == "POST":
        title = request.form["title"]
        isbn = request.form["isbn"]
        publication_year = request.form["publication_year"]
        author_id = request.form.get("author")  # Safe retrieval of author ID

        try:
            # Validate author_id
            if not author_id:
                flash("Author selection is required.", "danger")
                return redirect(url_for("add_book"))

            # Create the Book object
            new_book = Book(
                title=title,
                isbn=isbn,
                publication_year=int(publication_year),
                author_id=int(author_id),
            )

            # Save to the database
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully!", "success")
            return redirect(url_for("home"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {str(e)}", "danger")
            return redirect(url_for("add_book"))

    authors = Author.query.all()  # Fetch all authors for dropdown
    return render_template("add_book.html", authors=authors)


@app.route("/authors")
def authors():
    """
    Display the list of authors.

    Returns:
        Rendered HTML template for the authors page with a list of authors.
    """
    authors_list = Author.query.all()
    return render_template("authors.html", authors=authors_list)


@app.route("/author/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    """
    Delete an author from the database.

    Args:
        author_id (int): ID of the author to delete.

    Returns:
        Redirect to the authors page after deletion.
    """
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    flash("Author deleted successfully!", "success")
    return redirect(url_for("authors"))


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Delete a book from the database.

    If the book's author has no other books, the author is also deleted.

    Args:
        book_id (int): ID of the book to delete.

    Returns:
        Redirect to the home page after deletion.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author
    db.session.delete(book)
    db.session.commit()

    if author and not author.books:
        db.session.delete(author)
        db.session.commit()

    flash("Book deleted successfully!", "success")
    return redirect(url_for("home"))


def main():
    """
    Initialize the database and run the Flask application.
    """
    with app.app_context():
        db.create_all()
    app.run(debug=True)


if __name__ == "__main__":
    main()
