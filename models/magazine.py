import sqlite3

class Magazine:
    def __init__(self, id, name, category="General"):
        self._id = id
        self.name = name
        self.category = category
        
        # Check if the magazine already exists before inserting
        self._insert_into_database()

    def _insert_into_database(self):
        """Method to insert the magazine into the database."""
        # Establishing a connection to the database
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        # Create the magazines table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                          (id INTEGER PRIMARY KEY, name TEXT, category TEXT)''')
        
        # Check if the magazine already exists
        cursor.execute('SELECT id FROM magazines WHERE id = ?', (self._id,))
        existing_magazine = cursor.fetchone()
        
        if existing_magazine:
            print(f"Magazine with ID {self._id} already exists. Skipping insert.")
        else:
            # Insert the magazine into the table if it doesn't already exist
            cursor.execute(''' 
                INSERT INTO magazines (id, name, category) 
                VALUES (?, ?, ?)
            ''', (self._id, self.name, self.category))
            conn.commit()

        # Close the connection
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string")
        self._category = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    def __repr__(self):
        return f"<Magazine {self.name} - {self.category}>"
    
    # To retrieve the magazine from the database by id
    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Magazine(row[0], row[1], row[2])
        return None
import sqlite3

class Magazine:
    def __init__(self, id, name, category="General"):
        self._id = id
        self.name = name
        self.category = category
        
        # Check if the magazine already exists before inserting
        self._insert_into_database()

    def _insert_into_database(self):
        """Method to insert the magazine into the database."""
        # Establishing a connection to the database
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        # Create the magazines table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                          (id INTEGER PRIMARY KEY, name TEXT, category TEXT)''')
        
        # Check if the magazine already exists
        cursor.execute('SELECT id FROM magazines WHERE id = ?', (self._id,))
        existing_magazine = cursor.fetchone()
        
        if existing_magazine:
            print(f"Magazine with ID {self._id} already exists. Skipping insert.")
        else:
            # Insert the magazine into the table if it doesn't already exist
            cursor.execute(''' 
                INSERT INTO magazines (id, name, category) 
                VALUES (?, ?, ?)
            ''', (self._id, self.name, self.category))
            conn.commit()

        # Close the connection
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string")
        self._category = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    def __repr__(self):
        return f"<Magazine {self.name} - {self.category}>"
    
    # To retrieve the magazine from the database by id
    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Magazine(row[0], row[1], row[2])
        return None
