import sys

# Fonctions utilitaires:



# Gestion d'erreurs :

def is_valid_length(arguments):
    if len(arguments) != 2:
        print("Erreur : Merci d'indiquer deux arguments qui sont des chiffres")
        return False
    return True



# Récupération de données :
def get_arguments():
    arguments = sys.argv[1:]
    return arguments

# Résolution :

    
# Affichage :
