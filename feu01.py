import sys

# Fonctions utilitaires:
def tokenize_calculation(calculation: str) -> list[str]:
    tokenized_calculation = [] #Crée une liste vide pour stocker les tokens
    current_number = '' #Crée une chaîne vide pour accumuler les chiffres
    
    for char in calculation:
        if char.isdigit(): # Si le caractère est un chiffre (0-9)
            current_number += char ## Ajoute le chiffre à current_char
        elif char in '+-*/%()': # Si c'est un opérateur ou une parenthèse
            if current_number: # Si current_char contient des chiffres
                tokenized_calculation.append(current_number) # Ajoute le nombre à la liste
                current_number = ''  # Réinitialise current_char
            tokenized_calculation.append(char) # Ajoute l'opérateur/parenthèse à la liste
        elif char.isspace(): # Si c'est un espace
            if current_number: # Si current_char contient des chiffres
                tokenized_calculation.append(current_number) # Ajoute le nombre à la liste
                current_number = '' 
    
    if current_number: ## Si current_char contient encore des chiffres, Ajoute le dernier nombre à la liste
        tokenized_calculation.append(current_number)
    
    print(f"Tokens: {tokenized_calculation}")  # Ajout du print
    return tokenized_calculation


'''Cette fonction détermine la priorité des opérateurs :
	•	`+` et `-` ont une priorité de 1 
	•	`*`, `/` et `%` ont une priorité de 2 
	•	Les parenthèses ont une priorité de 0 (utilisée uniquement pour la comparaison)'''
def get_algo_shunting_yard(operator: str) -> int:
    if operator in ('+', '-'):
        return 1
    if operator in ('*', '/', '%'):
        return 2
    return 0  # pour les parenthèses

def get_reverse_polish_notation(tokens: list[str]) -> list[str]:
    output_queue = [] # Crée une liste vide pour stocker la sortie polish notation
    operator_stack = [] # Crée une pile vide pour stocker les opérateurs
    
    for token in tokens:
        if token.isdigit(): # Si le token est un nombre
            output_queue.append(token) # Ajoute directement le nombre à la sortie
            '''Avant d’ajouter un opérateur à la pile, on vérifie s’il y a des opérateurs de prio supérieure ou égale déjà dans la pile
		    Si c’est le cas, on les déplace vers la sortie
	 	    Cette étape garantit que les opérations de plus haute prio seront effectuées en premier'''
        elif token in '+-*/%':
            while (operator_stack and operator_stack[-1] != '(' and
                   get_algo_shunting_yard(operator_stack[-1]) >= get_algo_shunting_yard(token)):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(': # Ajoute la parenthèse ouvrante 
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
    while operator_stack:
        output_queue.append(operator_stack.pop())
    
    print(f"RPN: {output_queue}")  # Ajout du print
    return output_queue

def evaluate_reverse_polish_notation(polish_notation: list[str]) -> float:
    stack = []
    
    for token in polish_notation:
        if token.isdigit():
            stack.append(float(token))
        elif token in '+-*/%':
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            elif token == '%':
                result = a % b
            
            print(f"Opération: {a} {token} {b} = {result}")  # Ajout du print
            stack.append(result)
    
    return stack[0]

# Gestion d'erreurs :
def is_valid_length(arguments: list[str]) -> bool:
    if len(arguments) != 1:
        print("Erreur : Merci d'indiquer un seul argument entre guillemets representant le calcul")
        return False
    return True

# Récupération de données :
def get_arguments() -> list[str]:
    arguments = sys.argv[1:]
    return arguments

# Résolution :
def calculate_the_operation() -> None:
    arguments = get_arguments()

    if not is_valid_length(arguments):
        return

    calculation = arguments[0]

    tokens = tokenize_calculation(calculation)
    polish_notation = get_reverse_polish_notation(tokens)
    result = evaluate_reverse_polish_notation(polish_notation)
    
    print(f"Résultat final: {result}")  # Ajout du print

# Affichage :
calculate_the_operation()
