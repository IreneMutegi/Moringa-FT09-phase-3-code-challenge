from database.connection import get_db_connection

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

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS authors
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')

        if self.id is None:
            cursor.execute(''' 
                INSERT INTO authors (name) 
                VALUES (?)
            ''', (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute(''' 
                UPDATE authors 
                SET name = ? 
                WHERE id = ?
            ''', (self.name, self.id))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()

        conn.close()

        return [Author(id=author_data[0], name=author_data[1]) for author_data in authors_data]

    def articles(self):
        """Fetch all articles written by this author from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.id,))

        articles_data = cursor.fetchall()
        conn.close()

        return [Article(id=article_data[0], title=article_data[1], content=article_data[2], 
                        author_id=article_data[3], magazine_id=article_data[4]) 
                for article_data in articles_data]

    def magazines(self):
        """Fetch all magazines associated with this author from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.id,))

        magazines_data = cursor.fetchall()
        conn.close()

        return [Magazine(id=magazine_data[0], name=magazine_data[1], category=magazine_data[2]) 
                for magazine_data in magazines_data]
