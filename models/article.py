


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self._title=None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,value):
        if not isinstance(value,str) or not  ( 5 <= len(value) <=50):
            raise ValueError("title should be a string with characters between 5 and 50")
        if hasattr(self,'_title') and self._title is not None:
            raise AttributeError("cannot change title after it has been instantiated")
        self._title=value

    #fetches author associated with the article using SQL JOIN btw articles and author table
    def fetch_author(self):
        from database.connection import get_db_connection
        from .author import Author
        conn=get_db_connection()
        cursor=conn.cursor()
        query="""
         SELECT authors.* FROM articles
         JOIN authors ON articles.author_id = authors.id
         WHERE articles.id=?
        """
        cursor.execute(query,(self.id,))
        author_data=cursor.fetchone()
        conn.close()
        if author_data:
            return Author(author_data['id'],author_data['name'])
        else:
            return None
   
    #fetches magazine associated with the article using SQL JOIN btw articles and magazine table
    def fetch_magazine(self):
     from .magazine import Magazine
     from database.connection import get_db_connection
     conn = get_db_connection()
     cursor = conn.cursor()
     query = """
     SELECT magazines.* FROM articles
     JOIN magazines ON articles.magazine_id = magazines.id
     WHERE articles.id = ?
     """
     cursor.execute(query, (self.id,))
     magazine_data = cursor.fetchone()
     conn.close()
     if magazine_data:
        return Magazine(magazine_data['id'], magazine_data['name'], magazine_data['category'])
     else:
        return None

        

# def main():
#     db = Article()

#     while True:
#         print("\n1. Fetch Author")
#         print("2. Exit")

#         choice = input( "Ënter Choice")

#         if choice == "1":
#             id = int(input("Enter id :"))
#             db.fetch_author(id)
#         elif choice == "2":
#             db.close()
#             break
#         else:
#             print("Invalid choice")

if __name__ == "__main__":
    main()