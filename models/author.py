from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        if not isinstance(name, str) or len(name) == 0:
           raise ValueError("Name must be a non-empty string.")
        
        self._name = name
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
            self._id = cursor.lastrowid

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (self._id,)
            )
            return cursor.fetchall()

    def magazines(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.* 
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self._id,))
            return cursor.fetchall()

    def __repr__(self):
        return f'<Author {self.name}>'
