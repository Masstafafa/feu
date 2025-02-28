import sys

# Fonctions utilitaires:

def get_rectangle(length_of_rectangle: int, width_of_rectangle: int) -> str:
    if length_of_rectangle == 1 and width_of_rectangle == 1:
        return("o")
    
    rectangle = []
    if length_of_rectangle > 1:
        first_line = 'o' + ('-' * (length_of_rectangle - 2)) + 'o'
    else:
        first_line = 'o'
    rectangle.append(first_line)

    # Construire les lignes du milieu
    for _ in range(width_of_rectangle - 2):
        middle_line = '|' + (' ' * (length_of_rectangle - 2)) + '|'
        rectangle.append(middle_line)
    
    # Construire la dernière ligne (si nécessaire)
    if width_of_rectangle > 1:
        rectangle.append(first_line)

    return "\n".join(rectangle)

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
def display_rectangle() -> None:
    arguments = get_arguments()

    if not is_valid_length(arguments):
        return
    
    length_of_rectangle = arguments[0]
    width_of_rectangle = arguments[1]
    
    if not is_valid_rectangle(length_of_rectangle, width_of_rectangle):
        return
    
    length_of_rectangle = int(length_of_rectangle)
    width_of_rectangle = int(width_of_rectangle)

    rectangle_printed = get_rectangle(length_of_rectangle, width_of_rectangle)
    print(rectangle_printed)

    
# Affichage :

display_rectangle()
