import sys
from pathlib import Path


# Fonctions utilitaires:

def parse_grid(lines_of_sudoku):

    """Convertit le contenu du fichier en grille de Sudoku."""
    grid = []
    
    for line in lines_of_sudoku:
        row = []
        for char in line:
            if char == '.':
                row.append(0)  # 0 représente une case vide
            else:
                row.append(int(char))
        grid.append(row)
    
    return grid
        
def check_line(grid, index_line, value):
    for i in range(9):
        

# Gestion d'erreurs :

def is_valid_length(arguments: list[str]) -> bool:
    if len(arguments) != 1:
        print("Erreur : Merci d'indiquer un seul argument qui est le nom du fichier")
        return False
    return True

def is_valid_file(file_name: Path) -> bool:
    if not file_name.is_file():
        print(f"Erreur : le fichier {file_name} n'existe pas, veuillez rentrer un nom de fichier valide")
        return False
    return True

def is_valid_sudoku(lines_of_sudoku) -> bool:

    # Vérifie qu'il y a 9 lignes
    if len(lines_of_sudoku) != 9:
        print("Erreur : La grille doit contenir exactement 9 lignes")
        return False
    
    # Vérifier que chaque ligne a 9 caractères
    for i, line in enumerate(lines_of_sudoku):
        if len(line) != 9:
            print(f"Erreur : La ligne {i+1} ne contient pas 9 caractères")
            return False
        
        # Vérifier que chaque caractère est un chiffre de 1-9 ou un point
        for char in line:
            if char not in '123456789.':
                print(f"Erreur : Caractère invalide '{char}' trouvé")
                return False
    
    return True
    

# Récupération de données :

def get_arguments() -> list[str]:
    arguments = sys.argv[1:]
    return arguments

# Résolution :

def display_sudoku_solution() -> None:
    arguments = get_arguments()

    if not is_valid_length(arguments):
        return
    
    file_name = Path(arguments[0])

    if not is_valid_file(file_name):
        return
    
    content_of_file = file_name.read_text()
    lines_of_sudoku = content_of_file.split('\n')

    if not is_valid_sudoku(lines_of_sudoku):
        return
    
    grid = parse_grid(lines_of_sudoku)


    


# Affichage :

display_sudoku_solution()