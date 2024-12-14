class Author:
    def __init__(self, id, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self.id = id
        self._name = name  # Using a private attribute (_name) to prevent changes

    @property
    def name(self):
        return self._name  # Getter for the name attribute

    def __repr__(self):
        return f'<Author {self.name}>'

    def articles(self):
        pass

