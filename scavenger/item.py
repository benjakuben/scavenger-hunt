class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @id.setter
    def id(self, id):
        self.__id = id

    @name.setter
    def name(self, name):
        self.__name = name