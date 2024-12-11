from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the database.

    Attributes:
        id (int): Primary key for the Author.
        name (str): The name of the author.
        birth_date (date): The birth date of the author (optional).
        date_of_death (date): The date of death of the author (optional).
        books (list): List of books associated with the author.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        "Book", back_populates="author", cascade="all, delete-orphan"
    )

    def __str__(self):
        """
        Return a string representation of the Author.

        Returns:
            str: The name of the author.
        """
        return self.name


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (int): Primary key for the Book.
        isbn (str): The ISBN number of the book.
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author_id (int): Foreign key linking the book to an author.
        author (Author): The author associated with the book.
    """

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    author = db.relationship("Author", back_populates="books")

    def __str__(self):
        """
        Return a string representation of the Book.

        Returns:
            str: The title of the book.
        """
        return self.title
