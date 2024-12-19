from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title="", content="", author_id=None, magazine_id=None):
        self.id = id
        self._title = title
        self._content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be a string between 5 and 50 characters.")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._content = value
        else:
            raise ValueError("Content must be a non-empty string.")

    def __repr__(self):
        return f'<Article {self.title}>'

    def save(self):
        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author_id INTEGER, magazine_id INTEGER)''')

        if self.id is None:
            cursor.execute(''' 
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            ''', (self.title, self.content, self.author_id, self.magazine_id))

            self.id = cursor.lastrowid
        else:
            cursor.execute(''' 
                UPDATE articles 
                SET title = ?, content = ?, author_id = ?, magazine_id = ? 
                WHERE id = ? 
            ''', (self.title, self.content, self.author_id, self.magazine_id, self.id))

        conn.commit()
        conn.close()

    @property
    def author(self):
        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute('''
            SELECT authors.id, authors.name 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        ''', (self.id,))

        author_data = cursor.fetchone()
        conn.close()

        if author_data:
            return Author(id=author_data[0], name=author_data[1])
        return None

    @property
    def magazine(self):
        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute('''
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        ''', (self.id,))

        magazine_data = cursor.fetchone()
        conn.close()

        if magazine_data:
            return Magazine(id=magazine_data[0], name=magazine_data[1], category=magazine_data[2])
        return None

    @staticmethod
    def get_all():
        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM articles")
        articles_data = cursor.fetchall()
        conn.close()

        return [Article(id=article_data[0], title=article_data[1], content=article_data[2], author_id=article_data[3], magazine_id=article_data[4]) 
                for article_data in articles_data]
