class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    # Getter and Setter for title
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be a string between 5 and 50 characters.")

    # Getter and Setter for content
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

    def get_author(self):
        pass

    def get_magazine(self):
        pass
