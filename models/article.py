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
        """Save the article to the database."""
        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author_id INTEGER, magazine_id INTEGER)''')

        if self.id is None:
            # Insert a new article
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

    def get_author(self):
        """Fetch the author object for this article from the database."""
        from .author import Author

        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        author_data = cursor.fetchone()
        conn.close()

        if author_data:
            return Author(*author_data)  
        else:
            return None  

    def get_magazine(self):
        """Fetch the magazine object for this article from the database."""
        from .magazine import Magazine  
        conn = get_db_connection() 
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()

        if magazine_data:
            return Magazine(*magazine_data)  
        else:
            return None  
    @staticmethod
    def get_all():
        """Fetch all articles from the database."""
        conn = get_db_connection()  
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM articles")
        articles_data = cursor.fetchall()
        conn.close()

        return [Article(id=article_data[0], title=article_data[1], content=article_data[2], author_id=article_data[3], magazine_id=article_data[4]) 
                for article_data in articles_data]
