def valider_chaine(message):
    while True:
        saisi_input = input(message).strip()
        if saisi_input == '':
            print("La valeur ne doit pas vide")
        else:
            break

        if saisi_input.isnumeric():
            print('La saisi doit etre une chaine')
        else:
            break

        return saisi_input

def valider_email(message):
    while True:
        saisi_email =input(message).strip()

        if saisi_email == '':
            print("Valeur vide")
        else:
            break

        if "@" not in saisi_email and "." not in saisi_email and " " not in saisi_email:
            print("L'email saisi n'est pas valide")
        else:
            break

        return saisi_email

def valider_pwd(message):
    while True:
        mdp = input(message).strip()

        if len(mdp) < 4:
            print('le mot de pass doit contenir 4 caracteres')
        else:
            break

        return mdp