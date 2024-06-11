import unittest
import sqlite3
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection

def setup_test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    DROP TABLE IF EXISTS articles;
    DROP TABLE IF EXISTS authors;
    DROP TABLE IF EXISTS magazines;

    CREATE TABLE authors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE magazines (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL
    );

    CREATE TABLE articles (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER,
        magazine_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES authors(id),
        FOREIGN KEY (magazine_id) REFERENCES magazines(id)
    );

    INSERT INTO authors (id, name) VALUES (1, 'John Doe');
    INSERT INTO magazines (id, name, category) VALUES (1, 'Tech Weekly', 'Technology');
    INSERT INTO articles (id, title, content, author_id, magazine_id) VALUES (1, 'Test Title', 'Test Content', 1, 1);
    """)
    conn.commit()
    conn.close()

class TestModels(unittest.TestCase):
    def setUp(self):
        setup_test_db()

    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

class TestArticle(unittest.TestCase):
    def setUp(self):
        setup_test_db()
        self.article = Article(1, "Test Title", "Test Content", 1, 1)

    def test_article_initialization(self):
        self.assertEqual(self.article.id, 1)
        self.assertEqual(self.article.title, "Test Title")
        self.assertEqual(self.article.content, "Test Content")
        self.assertEqual(self.article.author_id, 1)
        self.assertEqual(self.article.magazine_id, 1)
    
    def test_article_title_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.article.title = "Too"
        with self.assertRaises(ValueError):
            self.article.title = "T" * 51
        with self.assertRaises(AttributeError):
            self.article.title = "New Title"

    def test_fetch_author(self):
        author = self.article.fetch_author()
        self.assertIsNotNone(author)
        self.assertEqual(author.id, 1)
        self.assertEqual(author.name, "John Doe")

    def test_fetch_magazine(self):
        magazine = self.article.fetch_magazine()
        self.assertIsNotNone(magazine)
        self.assertEqual(magazine.id, 1)
        self.assertEqual(magazine.name, "Tech Weekly")

class TestAuthor(unittest.TestCase):
    def setUp(self):
        setup_test_db()
        self.author = Author(1, "John Doe")

    def test_author_initialization(self):
        self.assertEqual(self.author.id, 1)
        self.assertEqual(self.author.name, "John Doe")

    def test_author_id_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.author.id = "one"

    def test_author_name_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.author.name = ""
        with self.assertRaises(AttributeError):
            self.author.name = "New Name"

    def test_articles(self):
        articles = self.author.articles()
        self.assertGreater(len(articles), 0)
        self.assertEqual(articles[0].author_id, self.author.id)

    def test_magazines(self):
        magazines = self.author.magazines()
        self.assertGreater(len(magazines), 0)
        self.assertEqual(magazines[0].id, 1)
        self.assertEqual(magazines[0].name, "Tech Weekly")

class TestMagazine(unittest.TestCase):
    def setUp(self):
        setup_test_db()
        self.magazine = Magazine(1, "Tech Weekly", "Technology")

    def test_magazine_initialization(self):
        self.assertEqual(self.magazine.id, 1)
        self.assertEqual(self.magazine.name, "Tech Weekly")
        self.assertEqual(self.magazine.category, "Technology")

    def test_magazine_id_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.magazine.id = "one"

    def test_magazine_name_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.magazine.name = "A"
        with self.assertRaises(ValueError):
            self.magazine.name = "A" * 17

    def test_magazine_category_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.magazine.category = ""

    def test_articles(self):
        articles = self.magazine.articles()
        self.assertGreater(len(articles), 0)
        self.assertEqual(articles[0].magazine_id, self.magazine.id)

    def test_contributors(self):
        contributors = self.magazine.contributors()
        self.assertGreater(len(contributors), 0)
        self.assertEqual(contributors[0].id, 1)
        self.assertEqual(contributors[0].name, "John Doe")

if __name__ == "__main__":
    unittest.main()
