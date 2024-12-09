from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        "Book", back_populates="author", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    author = db.relationship("Author", back_populates="books")

    def __str__(self):
        return self.title
