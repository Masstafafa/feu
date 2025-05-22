import sys
from pathlib import Path
from collections import deque

# Types personnalisés (sans typing pour éviter les conflits)
# Grid = List[List[str]]
# Position = Tuple[int, int]  
# Path = List[Position]

# Fonctions utilitaires
def parse_header(header_line: str):
    """Parse la première ligne (ex: '10x10* o12' -> (10, 10, '*', ' ', 'o', '1', '2'))."""
    if 'x' not in header_line:
        raise ValueError("Format invalide, 'x' manquant")
    
    # Séparer dimensions et caractères
    parts = header_line.split('x')
    if len(parts) != 2:
        raise ValueError("Format invalide")
    
    try:
        height = int(parts[0])
    except ValueError:
        raise ValueError("Hauteur invalide")
    
    # Parser la partie après 'x'
    remaining = parts[1]
    if len(remaining) < 6:  # Au minimum: largeur + 5 caractères
        raise ValueError("Pas assez de caractères")
    
    # Trouver où se termine la largeur (premier caractère non-digit)
    width_end = 0
    for i, char in enumerate(remaining):
        if not char.isdigit():
            width_end = i
            break
    
    if width_end == 0:
        raise ValueError("Largeur invalide")
    
    try:
        width = int(remaining[:width_end])
    except ValueError:
        raise ValueError("Largeur invalide")
    
    # Les 5 caractères suivants
    chars = remaining[width_end:width_end + 5]
    if len(chars) != 5:
        raise ValueError("Il faut exactement 5 caractères")
    
    wall_char = chars[0]
    empty_char = chars[1]
    path_char = chars[2]
    start_char = chars[3]
    end_char = chars[4]
    
    return height, width, wall_char, empty_char, path_char, start_char, end_char

def parse_grid(lines):
    """Convertit les lignes en grille 2D."""
    return [list(line) for line in lines]

def find_position(grid, target_char):
    """Trouve la position d'un caractère dans la grille."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == target_char:
                return (row, col)
    return None

def get_neighbors(position, grid):
    """Retourne les positions voisines valides (haut, bas, gauche, droite)."""
    row, col = position
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0])):
            neighbors.append((new_row, new_col))
    
    return neighbors

def find_all_positions(grid, target_char):
    """Trouve toutes les positions d'un caractère dans la grille."""
    positions = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == target_char:
                positions.append((row, col))
    return positions

def bfs_shortest_path_to_any_exit(grid, start, end_positions, empty_char, wall_char):
    """Trouve le plus court chemin vers n'importe quelle sortie."""
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current_pos, path = queue.popleft()
        
        # Vérifier si on a atteint une sortie
        if current_pos in end_positions:
            return path, current_pos
        
        for neighbor in get_neighbors(current_pos, grid):
            row, col = neighbor
            cell = grid[row][col]
            
            # On peut passer si c'est vide ou une sortie
            if neighbor not in visited and (cell == empty_char or neighbor in end_positions):
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
    
    return None, None

def fill_path(grid, path, path_char, start_char, end_char):
    """Remplit le chemin dans la grille (sans écraser start et end)."""
    for row, col in path:
        if grid[row][col] not in [start_char, end_char]:
            grid[row][col] = path_char

# Gestion d'erreurs
def is_valid_argument_count(arguments):
    """Vérifie qu'il y a exactement un argument."""
    if len(arguments) != 1:
        print("Erreur : Merci d'indiquer un seul argument qui est le nom du fichier")
        return False
    return True

def is_valid_file(file_path):
    """Vérifie que le fichier existe."""
    if not file_path.is_file():
        print(f"Erreur : le fichier {file_path} n'existe pas")
        return False
    return True

def has_minimum_lines(lines):
    """Vérifie qu'il y a au moins 2 lignes."""
    if len(lines) < 2:
        print("Erreur : Le fichier doit contenir au moins 2 lignes")
        return False
    return True

def has_correct_dimensions(lines, expected_height, expected_width):
    """Vérifie que les dimensions correspondent."""
    actual_height = len(lines) - 1  # -1 pour le header
    if actual_height != expected_height:
        print(f"Erreur : Hauteur annoncée {expected_height} mais {actual_height} lignes trouvées")
        return False
    
    for i, line in enumerate(lines[1:], 1):
        if len(line) != expected_width:
            print(f"Erreur : Largeur attendue {expected_width} mais ligne {i+1} fait {len(line)} caractères")
            return False
    
    return True

def has_valid_characters(lines, valid_chars):
    """Vérifie que la grille ne contient que les caractères autorisés."""
    for i, line in enumerate(lines[1:], 1):
        for char in line:
            if char not in valid_chars:
                print(f"Erreur : Caractère invalide '{char}' trouvé ligne {i+1}")
                return False
    return True

def has_start_and_end(grid, start_char, end_char):
    """Vérifie que l'entrée existe et qu'il y a au moins une sortie."""
    start_count = sum(row.count(start_char) for row in grid)
    end_count = sum(row.count(end_char) for row in grid)
    
    if start_count == 0:
        print(f"Erreur : Aucune entrée '{start_char}' trouvée")
        return False
    if start_count > 1:
        print(f"Erreur : Plusieurs entrées '{start_char}' trouvées")
        return False
    if end_count == 0:
        print(f"Erreur : Aucune sortie '{end_char}' trouvée")
        return False
    
    return True

# Récupération de données
def get_arguments():
    """Récupère les arguments de la ligne de commande."""
    return sys.argv[1:]

def read_file_lines(file_path):
    """Lit toutes les lignes du fichier."""
    content = file_path.read_text().rstrip('\n')
    return content.split('\n')

# Résolution
def solve_maze():
    """Fonction principale qui orchestre la résolution du labyrinthe."""
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
        height, width, wall_char, empty_char, path_char, start_char, end_char = parse_header(lines[0])
    except ValueError as e:
        print(f"Erreur dans le header : {e}")
        return
    
    # Validation des dimensions
    if not has_correct_dimensions(lines, height, width):
        return
    
    # Validation des caractères
    valid_chars = {wall_char, empty_char, start_char, end_char}
    if not has_valid_characters(lines, valid_chars):
        return
    
    # Parser la grille
    grid = parse_grid(lines[1:])
    
    # Vérifier entrée et sortie
    if not has_start_and_end(grid, start_char, end_char):
        return
    
    # Trouver positions de départ et toutes les sorties
    start_pos = find_position(grid, start_char)
    end_positions = find_all_positions(grid, end_char)
    
    if start_pos is None:
        print("Erreur : Impossible de trouver l'entrée")
        return
    
    if not end_positions:
        print("Erreur : Impossible de trouver les sorties")
        return
    
    # Trouver le plus court chemin vers n'importe quelle sortie
    path, chosen_exit = bfs_shortest_path_to_any_exit(grid, start_pos, end_positions, empty_char, wall_char)
    
    if path is None:
        print("Erreur : Aucun chemin trouvé entre l'entrée et les sorties")
        return
    
    # Remplir le chemin (exclut start et end du comptage)
    fill_path(grid, path, path_char, start_char, end_char)
    
    # Compter les coups (exclut la position de départ)
    moves = len(path) - 1
    
    return grid, moves

# Affichage
def display_result(grid, moves):
    """Affiche la grille résolue et le nombre de coups."""
    for row in grid:
        print(''.join(row))
    print(f"=> SORTIE ATTEINTE EN {moves} COUPS !")

def main():
    """Fonction principale du programme."""
    result = solve_maze()
    if result:
        grid, moves = result
        display_result(grid, moves)

if __name__ == "__main__":
    main()