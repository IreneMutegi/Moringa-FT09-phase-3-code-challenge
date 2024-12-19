from database.connection import get_db_connection  
from .article import Article  

class Author:
    def __init__(self, id=None, name=""):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self.id = id
        self._name = name  

    @property
    def name(self):
        return self._name  

    def __repr__(self):
        return f'<Author {self.name}>'

    def articles(self):
        """Fetch all articles written by this author from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles_data = cursor.fetchall()

        conn.close()

        return [Article(*article_data) for article_data in articles_data]

    def save(self):
        """Save the author to the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            self.id = cursor.lastrowid 
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self.id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        """Fetch all authors from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()

        conn.close()

        return [Author(id=author_data[0], name=author_data[1]) for author_data in authors_data]
