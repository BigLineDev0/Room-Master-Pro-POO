class Reservation:

    def __init__(self, id_creneau, id_groupe, type_evenement, statut="Valide", _id=None):
        self.__id = _id
        self.__id_creneau = id_creneau
        self.__id_groupe = id_groupe
        self.__type_evenement = type_evenement
        self.__statut = statut

    @property
    def id(self):
        return self.__id

    @property
    def id_creneau(self):
        return self.__id_creneau

    @property
    def id_groupe(self):
        return self.__id_groupe

    @property
    def type_evenement(self):
        return self.__type_evenement

    @property
    def statut(self):
        return self.__statut
    
    def __str__(self):
        return f"{self.id_creneau} - {self.id_groupe} - {self.type_evenement} - {self.statut}"