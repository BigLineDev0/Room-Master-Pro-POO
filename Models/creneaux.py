class Creneau:

    def __init__(self, heure_debut, heure_fin, _id=None):
        self.__id = _id
        self.__heure_debut = heure_debut
        self.__heure_fin = heure_fin

        if heure_debut >= heure_fin:
            raise ValueError("L'heure de début doit être avant l'heure de fin")

    @property
    def id(self):
        return self.__id
    
    @property
    def heure_debut(self):
        return self.__heure_debut

    @property
    def heure_fin(self):
        return self.__heure_fin
    

    def __str__(self):
        return f"{self.heure_debut} - {self.heure_fin}"