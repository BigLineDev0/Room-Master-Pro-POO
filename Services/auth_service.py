from Repositories.utilisateur_repository import UserRepository
import bcrypt

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def inscription(self, nom, prenom, email, password):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.user_repo.enregistrer(nom, prenom, email, password_hash)

    def connexion(self, email, password):
        user = self.user_repo.trouver_par_email(email)

        if not user:
            print("Utilisateur introuvable")
            return None
        
        if not bcrypt.checkpw(password.encode(), user.mot_de_passe.encode()):
            return None
        
        return user