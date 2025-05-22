import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Types personnalisés
Grid = List[List[str]]
Position = Tuple[int, int]
Square = Tuple[Position, int]  # ((row, col), size)

# Fonctions utilitaires
def parse_header(header_line: str) -> Tuple[int, str, str, str]:
    """Parse la première ligne du fichier (ex: '9.xo' -> (9, '.', 'x', 'o'))."""
    if len(header_line) < 4:
        raise ValueError("Header trop court")
    
    # Les 3 derniers caractères sont empty, obstacle, full
    empty_char = header_line[-3]
    obstacle_char = header_line[-2]
    full_char = header_line[-1]
    
    # Tout ce qui précède est la hauteur
    height_str = header_line[:-3]
    
    if not height_str:
        raise ValueError("Aucune hauteur spécifiée")
    
    try:
        height = int(height_str)
    except ValueError:
        raise ValueError("Hauteur invalide")
    
    if height <= 0:
        raise ValueError("La hauteur doit être positive")
    
    return height, empty_char, obstacle_char, full_char

def parse_grid(lines: List[str], empty_char: str, obstacle_char: str) -> Grid:
    """Convertit les lignes en grille 2D."""
    grid = []
    for line in lines:
        row = list(line)
        grid.append(row)
    return grid

def is_valid_square_at_position(grid: Grid, row: int, col: int, size: int, empty_char: str) -> bool:
    """Vérifie si on peut placer un carré de taille donnée à une position."""
    rows, cols = len(grid), len(grid[0])
    
    # Vérifier les limites
    if row + size > rows or col + size > cols:
        return False
    
    # Vérifier que toutes les cases sont vides
    for i in range(row, row + size):
        for j in range(col, col + size):
            if grid[i][j] != empty_char:
                return False
    
    return True

def find_largest_square(grid: Grid, empty_char: str) -> Optional[Square]:
    """Trouve le plus grand carré possible (en haut à gauche en cas d'égalité)."""
    if not grid or not grid[0]:
        return None
    
    rows, cols = len(grid), len(grid[0])
    max_size = 0
    best_position = None
    
    # Tester toutes les positions et toutes les tailles
    for row in range(rows):
        for col in range(cols):
            # Tester les tailles croissantes à partir de cette position
            max_possible_size = min(rows - row, cols - col)
            for size in range(1, max_possible_size + 1):
                if is_valid_square_at_position(grid, row, col, size, empty_char):
                    if size > max_size:
                        max_size = size
                        best_position = (row, col)
                else:
                    break  # Si cette taille ne marche pas, les plus grandes non plus
    
    if best_position is None:
        return None
    
    return best_position, max_size

def fill_square(grid: Grid, position: Position, size: int, full_char: str) -> None:
    """Remplit un carré avec le caractère plein."""
    row, col = position
    for i in range(row, row + size):
        for j in range(col, col + size):
            grid[i][j] = full_char

# Gestion d'erreurs
def is_valid_argument_count(arguments: List[str]) -> bool:
    """Vérifie qu'il y a exactement un argument."""
    if len(arguments) != 1:
        print("Erreur : Merci d'indiquer un seul argument qui est le nom du fichier")
        return False
    return True

def is_valid_file(file_path: Path) -> bool:
    """Vérifie que le fichier existe."""
    if not file_path.is_file():
        print(f"Erreur : le fichier {file_path} n'existe pas")
        return False
    return True

def has_minimum_lines(lines: List[str]) -> bool:
    """Vérifie qu'il y a au moins 2 lignes (header + au moins une ligne de carte)."""
    if len(lines) < 2:
        print("Erreur : Le fichier doit contenir au moins 2 lignes")
        return False
    return True

def has_correct_height(lines: List[str], expected_height: int) -> bool:
    """Vérifie que le nombre de lignes correspond à la hauteur annoncée."""
    actual_lines = len(lines) - 1  # -1 pour exclure le header
    if actual_lines != expected_height:
        print(f"Erreur : Hauteur annoncée {expected_height} mais {actual_lines} lignes trouvées")
        return False
    return True

def has_uniform_line_length(lines: List[str]) -> bool:
    """Vérifie que toutes les lignes de la carte ont la même longueur."""
    if len(lines) < 2:
        return True
    
    expected_length = len(lines[1])
    for i, line in enumerate(lines[1:], 1):
        if len(line) != expected_length:
            print(f"Erreur : La ligne {i+1} a une longueur différente")
            return False
    return True

def has_valid_characters(lines: List[str], empty_char: str, obstacle_char: str) -> bool:
    """Vérifie que la carte ne contient que les caractères autorisés."""
    valid_chars = {empty_char, obstacle_char}
    
    for i, line in enumerate(lines[1:], 1):
        for char in line:
            if char not in valid_chars:
                print(f"Erreur : Caractère invalide '{char}' trouvé ligne {i+1}")
                return False
    return True

def has_minimum_size(lines: List[str]) -> bool:
    """Vérifie qu'il y a au moins une ligne d'une case."""
    if len(lines) < 2:
        return False
    if len(lines[1]) < 1:
        print("Erreur : La carte doit avoir au moins une case")
        return False
    return True

# Récupération de données
def get_arguments() -> List[str]:
    """Récupère les arguments de la ligne de commande."""
    return sys.argv[1:]

def read_file_lines(file_path: Path) -> List[str]:
    """Lit toutes les lignes du fichier."""
    content = file_path.read_text().rstrip('\n')
    return content.split('\n')

# Résolution
def solve_largest_square() -> Optional[Grid]:
    """Fonction principale qui orchestre la résolution du problème."""
    arguments = get_arguments()
    
    if not is_valid_argument_count(arguments):
        return
    
    file_path = Path(arguments[0])
    
    if not is_valid_file(file_path):
        return
    
    lines = read_file_lines(file_path)
    
    if not has_minimum_lines(lines):
        return
    
    # Parser le header
    try:
        height, empty_char, obstacle_char, full_char = parse_header(lines[0])
    except ValueError as e:
        print(f"Erreur dans le header : {e}")
        return
    
    # Validation de la carte
    if not has_correct_height(lines, height):
        return
    
    if not has_uniform_line_length(lines):
        return
    
    if not has_minimum_size(lines):
        return
    
    if not has_valid_characters(lines, empty_char, obstacle_char):
        return
    
    # Parser la grille
    grid = parse_grid(lines[1:], empty_char, obstacle_char)
    
    # Trouver et remplir le plus grand carré
    square_info = find_largest_square(grid, empty_char)
    
    if square_info is not None:
        position, size = square_info
        fill_square(grid, position, size, full_char)
    
    return grid

# Affichage
def display_grid(grid: Grid) -> None:
    """Affiche la grille résultat."""
    for row in grid:
        print(''.join(row))

def main() -> None:
    """Fonction principale du programme."""
    result_grid = solve_largest_square()
    if result_grid:
        display_grid(result_grid)

if __name__ == "__main__":
    main()