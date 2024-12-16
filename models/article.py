from database.connection import get_db_connection

class Article:
    def __init__(self, author, magazine, title):
        if not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters.")
        
        self._title = title
        self._author = author
        self._magazine = magazine
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)",
                (author.id, magazine.id, title)
            )
            self._id = cursor.lastrowid

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    def __repr__(self):
        return f'<Article {self.title}>'
