import sqlite3

class Magazine:
    def __init__(self, id=None, name="", category="General"):
        """Constructor to create a new magazine or load an existing one."""
        self.id = id
        self._name = name
        self._category = category
        
        # If no ID is passed, insert into the database and auto-generate the ID
        if id is None:
            self.save()  # Automatically save to DB if the magazine doesn't exist
    
    def save(self):
        """Save the magazine to the database."""
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        # Create the magazines table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT)''')

        if self.id is None:
            # Insert a new magazine into the database
            cursor.execute(''' 
                INSERT INTO magazines (name, category) 
                VALUES (?, ?)
            ''', (self.name, self.category))

            # Get the auto-generated id and assign it to the instance
            self.id = cursor.lastrowid
        else:
            # Update an existing magazine
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
        """Retrieve all magazines from the database."""
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()

        # Return a list of Magazine objects
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]
