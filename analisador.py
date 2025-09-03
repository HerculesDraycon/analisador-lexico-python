import re
# Definicao dos padroes de tokens
token_specification = [
    ("NUMBER",   r'\d+(\.\d*)?'),   # Numeros inteiros ou decimais
    ("ID",       r'[A-Za-z_]\w*'),  # Identificadores
    ("OP",       r'[+\-*/]'),       # Operadores
    ("SKIP",     r'[ \t]+'),        # Espaços e tabulacoes
    ("MISMATCH", r'.'),             # Qualquer coisa inesperada
]

tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

def lexer(code):
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f"Caractere inválido em {pos}")
        kind = match.lastgroup
        value = match.group()
        if kind != "SKIP" and kind != "MISMATCH":
            yield kind, value
        pos = match.end()

print("Digite uma expressão:")
exp = input()

tokens = list(lexer(exp))
print(tokens)