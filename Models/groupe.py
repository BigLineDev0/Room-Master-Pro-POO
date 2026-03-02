class Groupe:
    def __init__(self, nom, responsable, _id=None):
        self.__id = _id
        self.__nom = nom
        self.__responsable = responsable

    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    @property
    def responsable(self):
        return self.__responsable
    
    def __str__(self):
        return f"{self.nom} - {self.responsable}"