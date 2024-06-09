from database.connection import get_db_connection
from article import Article
from magazine import Magazine
class Author:
    def __init__(self, id, name):
        self._id=None
        self.id = id
        self._name=None
        self.name = name
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,value):
        if not isinstance(value,int):
            raise ValueError("id must be an Integer")
        self._id=value

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        if not isinstance(value,str) or len(value)<=0:
            raise ValueError("name must be a string with characters longer than 0")
        if hasattr(self,'_name') and self._name is not None:
            raise AttributeError("Cannot change name after it is set")
        self._name=value

    def __repr__(self):
        return f'<Author {self.name}>'
    
    #fetches ALL the articles assoiated wwith the author
    def articles(self):
     conn=get_db_connection()
     cursor=conn.cursor()
     query="""
      SELECT articles.* FROM articles
      JOIN authors ON articles.author_id=authors.id
      WHERE authors.id=?
      """
     cursor.execute(query,(self.id,))
     articles_data=cursor.fetchall()
     conn.close()
     
     articles=[]
     for article_data in articles_data:
        articles.append(Article(article_data['id'],article_data['title'],article_data['content'],article_data['author_id'],article_data['magazine_id']))
     return articles
    
    #fetches ALL the magazines associated with the author
    def magazines(self):
     conn=get_db_connection()
     cursor=conn.cursor()
     query="""
      SELECT magazines.* FROM magazines
      JOIN articles ON magazines.id=articles.magazine_id
      JOIN authors ON articles.author_id=authors.id
      WHERE authors.id=?
      """
     cursor.execute(query,(self.id,))
     magazines_data=cursor.fetchall()
     conn.close()

     magazines=[]
     for magazine_data in magazines_data:
        magazines.append(Magazine(magazine_data['id'],magazine_data['title'],magazine_data['content'],magazine_data['author_id'],magazine_data['magazine_id']))
     return magazines