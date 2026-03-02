from Repositories.groupe_repository import GroupeRepository

class GroupeService:
    def __init__(self):
        self.groupe_repo = GroupeRepository()

    def creer_groupe(self, groupe):
        if self.groupe_repo.exist_groupe(groupe.nom, groupe.responsable):
            raise Exception("Ce groupe existe deja.")
        
        self.groupe_repo.enregistrer(groupe)

    def lister_groupe(self):
        return self.groupe_repo.afficher_tout()