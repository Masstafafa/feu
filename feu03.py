import sys
from pathlib import Path
from typing import Optional, Tuple, List

############################# Fonctions utilitaires ############################
def parse_grid(lines_of_sudoku: List[str]) -> List[List[int]]:
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

def check_line(grid: List[List[int]], row: int, value: int) -> bool:
    """Vérifie si une valeur peut être placée dans une ligne."""
    return value not in grid[row]

def check_column(grid: List[List[int]], col: int, value: int) -> bool:
    """Vérifie si une valeur peut être placée dans une colonne."""
    for row in range(9):
        if grid[row][col] == value:
            return False
    return True

def check_box(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Vérifie si une valeur peut être placée dans le carré 3x3."""
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == value:
                return False
    return True

def is_valid_move(grid: List[List[int]], row: int, col: int, value: int) -> bool:
    """Vérifie si un mouvement est valide selon les règles du Sudoku."""
    return (check_line(grid, row, value) and 
            check_column(grid, col, value) and 
            check_box(grid, row, col, value))

def find_empty_cell(grid: List[List[int]]) -> Tuple[Optional[int], Optional[int]]:
    """Trouve la première case vide dans la grille."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None, None

def solve_sudoku(grid: List[List[int]]) -> bool:
    """Résout le Sudoku en utilisant le backtracking récursif."""
    row, col = find_empty_cell(grid)
    
    # Si aucune case vide, le Sudoku est résolu
    if row is None:
        return True
    
    # Essayer les chiffres de 1 à 9
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            # Récursion : essayer de résoudre le reste
            if solve_sudoku(grid):
                return True
            
            # Backtracking : annuler le mouvement
            grid[row][col] = 0
    
    return False

############################# Gestion d'erreurs ############################
def is_valid_length(arguments: List[str]) -> bool:
    """Vérifie que le bon nombre d'arguments est fourni."""
    if len(arguments) != 1:
        print("Erreur : Merci d'indiquer un seul argument qui est le nom du fichier")
        return False
    return True

def is_valid_file(file_name: Path) -> bool:
    """Vérifie que le fichier existe."""
    if not file_name.is_file():
        print(f"Erreur : le fichier {file_name} n'existe pas, veuillez rentrer un nom de fichier valide")
        return False
    return True

def has_correct_line_count(lines_of_sudoku: List[str]) -> bool:
    """Vérifie que la grille contient exactement 9 lignes."""
    if len(lines_of_sudoku) != 9:
        print("Erreur : La grille doit contenir exactement 9 lignes")
        return False
    return True

def has_correct_line_length(lines_of_sudoku: List[str]) -> bool:
    """Vérifie que chaque ligne contient exactement 9 caractères."""
    for i, line in enumerate(lines_of_sudoku):
        if len(line) != 9:
            print(f"Erreur : La ligne {i+1} ne contient pas 9 caractères")
            return False
    return True

def has_valid_characters(lines_of_sudoku: List[str]) -> bool:
    """Vérifie que chaque caractère est un chiffre de 1-9 ou un point."""
    for line in lines_of_sudoku:
        for char in line:
            if char not in '123456789.':
                print(f"Erreur : Caractère invalide '{char}' trouvé")
                return False
    return True

# Récupération de données
def get_arguments() -> List[str]:
    """Récupère les arguments de la ligne de commande."""
    return sys.argv[1:]

############################# Résolution ############################
def solve_sudoku_from_file() -> Optional[List[List[int]]]:
    """Fonction principale qui orchestre la résolution du Sudoku."""
    arguments = get_arguments()

    if not is_valid_length(arguments):
        return
    
    file_name = Path(arguments[0])

    if not is_valid_file(file_name):
        return
    
    content_of_file = file_name.read_text().strip()
    lines_of_sudoku = content_of_file.split('\n')

    # Validation du format en 3 étapes distinctes
    if not has_correct_line_count(lines_of_sudoku):
        return
    
    if not has_correct_line_length(lines_of_sudoku):
        return
    
    if not has_valid_characters(lines_of_sudoku):
        return
    
    grid = parse_grid(lines_of_sudoku)
    
    if solve_sudoku(grid):
        return grid
    else:
        print("Erreur : Ce Sudoku n'a pas de solution")
        return

############################ Affichage ############################
def display_grid(grid: List[List[int]]) -> None:
    """Affiche la grille de Sudoku résolue."""
    for row in grid:
        print(''.join(map(str, row)))

def main() -> None:
    """Fonction principale du programme."""
    solved_grid = solve_sudoku_from_file()
    if solved_grid:
        display_grid(solved_grid)

if __name__ == "__main__":
    main()