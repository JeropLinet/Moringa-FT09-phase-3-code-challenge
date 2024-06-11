from database.connection import get_db_connection


class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category

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
     from .article import Article
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
     from .author import Author
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
    
    
    def article_titles(self):
        conn=get_db_connection()
        cursor=conn.cursor()
        query="""
          SELECT title FROM articles
          WHERE magazine_id=?
        """
        cursor.execute(query,(self.id,))
        titles_data=cursor.fetchall()
        conn.close

        if not titles_data:
            return None
        #the strings of titles are returned
        titles=[title['title'] for title in titles_data]
        return titles
    
    def contributing_authors(self):
        conn=get_db_connection()
        cursor=conn.cursor()
        query="""
        SELECT authors_id,COUNT(*) as article_count FROM articles
        WHERE magazine_id=?
        GROUP BY author_id
        HAVING article_count > 2
        """
        cursor.execute(query,(self.id,))
        authors_data=cursor.fetchall()
        conn.close

        authors=[]
        for author_data in authors_data:
            author_id=author_data['author_id']
            author=Author.get_by_id(author_id)
            if author:
                authors.append(author)
        if authors:
            return authors
        else:
            return None