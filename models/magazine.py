from database.connection import get_db_connection
from .article import Article 
from .author import Author  

class Magazine:
    def __init__(self, id=None, name="", category="General"):
        self.id = id
        self._name = name
        self._category = category

        if id is None:
            self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT)''')

        if self.id is None:
            cursor.execute(''' 
                INSERT INTO magazines (name, category) 
                VALUES (?, ?)
            ''', (self.name, self.category))
            self.id = cursor.lastrowid
        else:
            cursor.execute(''' 
                UPDATE magazines 
                SET name = ?, category = ? 
                WHERE id = ?
            ''', (self.name, self.category, self.id))

        conn.commit()
        conn.close()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def __repr__(self):
        return f"<Magazine {self.name} - {self.category}>"

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()

        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

    def articles(self):
        """Fetch all articles associated with this magazine from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self.id,))

        articles_data = cursor.fetchall()
        conn.close()

        return [Article(id=article_data[0], title=article_data[1], content=article_data[2], 
                        author_id=article_data[3], magazine_id=article_data[4]) 
                for article_data in articles_data]

    def contributors(self):
        """Fetch all authors associated with this magazine from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self.id,))

        contributors_data = cursor.fetchall()
        conn.close()

        return [Author(id=author_data[0], name=author_data[1]) for author_data in contributors_data]

    def article_titles(self):
        """Return a list of article titles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))

        titles_data = cursor.fetchall()
        conn.close()

        if titles_data:
            return [title[0] for title in titles_data]
        return None

    def contributing_authors(self):
        """Return authors who have written more than 2 articles for this magazine."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))

        authors_data = cursor.fetchall()
        conn.close()

        if authors_data:
            return [Author(id=author_data[0], name=author_data[1]) for author_data in authors_data]
        return None
