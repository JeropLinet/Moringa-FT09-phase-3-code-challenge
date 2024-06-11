import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
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
        self.assertEqual(author.name, "Author Name")

    def test_fetch_magazine(self):
        magazine = self.article.fetch_magazine()
        self.assertIsNotNone(magazine)
        self.assertEqual(magazine.id, 1)
        self.assertEqual(magazine.name, "Magazine Name")

class TestAuthor(unittest.TestCase):
    def setUp(self):
        self.author = Author(1, "Author Name")

    def test_author_initialization(self):
        self.assertEqual(self.author.id, 1)
        self.assertEqual(self.author.name, "Author Name")

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
        self.assertEqual(magazines[0].name, "Magazine 1")

class TestMagazine(unittest.TestCase):
    def setUp(self):
        self.magazine = Magazine(1, "Magazine Name", "Category")

    def test_magazine_initialization(self):
        self.assertEqual(self.magazine.id, 1)
        self.assertEqual(self.magazine.name, "Magazine Name")
        self.assertEqual(self.magazine.category, "Category")

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
        self.assertEqual(contributors[0].name, "Author 1")

if __name__ == "__main__":
    unittest.main()
