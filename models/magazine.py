from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        if not (2 <= len(name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")
        if len(category) == 0:
            raise ValueError("Category must be non-empty.")
        
        self.id = id
        self.name = name
        self.category = category
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)", 
                (name, category)
            )
            self._id = cursor.lastrowid

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters.")
        self._name = value
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE magazines SET name = ? WHERE id = ?", 
                (value, self._id)
            )

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) == 0:
            raise ValueError("Category must be non-empty.")
        self._category = value
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE magazines SET category = ? WHERE id = ?", 
                (value, self._id)
            )

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (self._id,)
            )
            return cursor.fetchall()

    def contributors(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT a.* 
                FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
            """, (self._id,))
            return cursor.fetchall()

    def article_titles(self):
        articles = self.articles()
        return [article[3] for article in articles] if articles else None

    def contributing_authors(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, COUNT(art.id) as count 
                FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
                GROUP BY a.id
                HAVING count > 2
            """, (self._id,))
            return cursor.fetchall()         


    def __repr__(self):
        return f'<Magazine {self.name}>'
