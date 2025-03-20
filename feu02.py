import sys
from pathlib import Path


# Fonctions utilitaires:

def transform_board_into_list_of_lists(board):
    board_list = []
    content_of_board = board.read_text()
    lines = content_of_board.splitlines()

    for line in lines:
        char_list = list(line)
        board_list.append(char_list)
    return board_list


def find_position_on_board(board_list, board_to_find_list):
    for y in range(len(board_list)):
        for x in range(len(board_list[0])):
            if check_match(board_list, board_to_find_list, x, y):
                return(f"Trouvé !\nCoordonnées : {x},{y}")
    return("Introuvable")

def check_match(board, board_to_find, x, y):
    for i in range(len(board_to_find)):
        for j in range(len(board_to_find[0])):
            # Vérifie si on ne dépasse pas les limites de board
            if y + i >= len(board) or x + j >= len(board[0]):
                return False
            # Compare le caractère de boardtofind avec celui de board
            if board_to_find[i][j] != ' ' and board_to_find[i][j] != board[y + i][x + j]:
                return False
    return True

  
# Gestion d'erreurs :

def is_valid_length(arguments: list[str]) -> bool:
    if len(arguments) != 2:
        print("Erreur : Merci d'indiquer deux arguments qui sont les noms de fichiers que vous "
        "souhaitez comparer")
        return False
    return True

def is_valid_file(arguments: list[str]) -> bool:
    all_files_exist = True
    for argument in arguments:
        file_name = Path(argument)
        if not file_name.is_file():
            print(f"Erreur : le fichier {file_name} n'existe pas, veuillez rentrer un nom de fichier valide")
            all_files_exist = False
    return all_files_exist

# Récupération de données :
def get_arguments() -> list[str]:
    arguments = sys.argv[1:]
    return arguments

# Résolution :


def resolve():
    arguments = get_arguments()

    if not is_valid_length(arguments):
        return

    if not is_valid_file(arguments):
        return
    
    board = Path(arguments[0])
    board_to_find = Path(arguments[1])

    board_list = transform_board_into_list_of_lists(board)
    board_to_find_list = transform_board_into_list_of_lists(board_to_find)

    print(find_position_on_board(board_list, board_to_find_list))

# Affichage :
resolve()