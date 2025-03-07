import sys

# Fonctions utilitaires:


# Gestion d'erreurs :

def is_valid_length(arguments: list[str]) -> bool:
    if len(arguments) != 2:
        print("Erreur : Merci d'indiquer deux arguments qui sont des chiffres")
        return False
    return True

def is_valid_rectangle(length_of_rectangle: str, width_of_rectangle: str) -> bool:
    if not length_of_rectangle.isdigit():
        print("Erreur : Merci d'indiquer la longueur avec un chiffre entier")
        return False
    if not width_of_rectangle.isdigit():
        print("Erreur : Merci d'indiquer la largeur avec un chiffre entier")
        return False
    return True

# Récupération de données :
def get_arguments() -> list[str]:
    arguments = sys.argv[1:]
    return arguments

# Résolution :

arguments = get_arguments()

 
    
# Affichage :
