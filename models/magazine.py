from database.connection import get_db_connection
from article import Article
from author import Author
class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,value):
        if not isinstance(value,int):
            raise ValueError("id must be an int")
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        if not isinstance(value,str) or len(value)<2 or len(value)>16:
            raise ValueError("name must be a string that is between 2 and 16 characters")
        self._name=value

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self,value):
        if not isinstance(value,str) or len(value) <= 0:
            raise ValueError("category must be a string that is longer than 0")

    def articles(self):
     conn=get_db_connection()
     cursor=conn.cursor()
     query="""
      SELECT articles.* FROM articles
      JOIN magazines ON articles.magazine_id=magazines.id
      WHERE magazines.id=?
      """
     cursor.execute(query,(self.id,))
     articles_data=cursor.fetchall()
     conn.close()
     
     articles=[]
     for article_data in articles_data:
        articles.append(Article(article_data['id'],article_data['name'],article_data['category']))
     return articles
    
    def contributors(self):
     conn=get_db_connection()
     cursor=conn.cursor()
     query="""
      SELECT authors.* FROM articles
      JOIN magazines ON authors.magazine_id=magazines.id
      WHERE magazines.id=?
      """
     cursor.execute(query,(self.id,))
     authors_data=cursor.fetchall()
     conn.close()
     
     contributors=[]
     for author_data in authors_data:
        contributors.append(Author(author_data['id'],author_data['name'],author_data['category']))
     return contributors
    
    