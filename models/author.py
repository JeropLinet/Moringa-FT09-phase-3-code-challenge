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
