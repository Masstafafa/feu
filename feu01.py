import sys

# Fonctions utilitaires:
def tokenize_calculation(calculation: str) -> list[str]:
    tokenized_calculation = []
    current_number = ''
    
    for char in calculation:
        if char.isdigit():
            current_number += char
        elif char in '+-*/%()':
            if current_number:
                tokenized_calculation.append(current_number)
                current_number = ''
            tokenized_calculation.append(char)
        elif char.isspace():
            if current_number:
                tokenized_calculation.append(current_number)
                current_number = ''
    
    if current_number:
        tokenized_calculation.append(current_number)
    
    print(f"Tokens: {tokenized_calculation}")  # Ajout du print
    return tokenized_calculation

def get_algo_shunting_yard(operator: str) -> int:
    if operator in ('+', '-'):
        return 1
    if operator in ('*', '/', '%'):
        return 2
    return 0  # pour les parenthèses

def get_reverse_polish_notation(tokens: list[str]) -> list[str]:
    output_queue = []
    operator_stack = []
    
    for token in tokens:
        if token.isdigit():
            output_queue.append(token)
        elif token in '+-*/%':
            while (operator_stack and operator_stack[-1] != '(' and
                   get_algo_shunting_yard(operator_stack[-1]) >= get_algo_shunting_yard(token)):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
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
        print("Erreur : Merci d'indiquer un seul argument representant le calcul")
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
