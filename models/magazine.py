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


    