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
        if not isinstance(value,str) or len(value) <=5 or len(value) >=50:
            raise ValueError("title should be a string with characters between 5 and 50")
        if hasattr(self,'_title') and self._title is not None:
            raise AttributeError("cannot change title after it has been instantiated")
        self._title=value