class Utilisateur:
    def __init__(self, nom, prenom, email, mot_de_passe, _id=None, role="admin"):
        self.__id = _id
        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__role = role
    
    # Getters
    @property
    def id(self):
        return self.__id

    @property
    def nom(self):
        return self.__nom

    @property
    def prenom(self):
        return self.__prenom

    @property
    def email(self):
        return self.__email

    @property
    def mot_de_passe(self):
        return self.__mot_de_passe

    @property
    def role(self):
        return self.__role

    def __str__(self):
        return f"{self.prenom} { self.nom} - {self.mail}"