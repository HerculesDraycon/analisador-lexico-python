import re
arquivo_de_entrada = "entrada.txt"
arquivo_de_saida = "saida.txt"

palavras_reservadas = {
    "ABSOLUTE", "AND", "ARRAY", "BEGIN", "CASE", "CHAR", "CONST", "DIV", "DO",
    "DOWNTO", "ELSE", "END", "EXTERNAL", "FILE", "FOR", "FORWARD", "FUNC",
    "FUNCTION", "GOTO", "IF", "IMPLEMENTATION", "INTEGER", "INTERFACE",
    "INTERRUPT", "LABEL", "MAIN", "NIL", "NIT", "NOT", "OF", "OR", "PACKED",
    "PROC", "PROGRAM", "REAL", "RECORD", "REPEAT", "SET", "SHL", "SHR",
    "STRING", "THEN", "TO", "TYPE", "UNIT", "UNTIL", "USES", "VAR",
    "WHILE", "WITH", "XOR"
}

# Definicao dos padroes de tokens
token_specification = [
    ("COMMENT",       r'/\*.*?\*/'),             # Comentarios
    ("STRING",        r'"[^"]*"'),               # Strings delimitadas por aspas duplas
    ("CHAR",          r"'[^']*'"),               # Caracteres delimitados por aspas simples
    ("NUMBER",        r'\d+(\.\d*)?'),           # Numeros inteiros ou decimais
    ("BLOCK",         r'\b(begin|end)\b'),       # Blocos de comandos
    ("CONDITIONAL",   r'\b(if|then|else)\b'),    # Condicionais
    ("LOOP",          r'\b(while|do)\b'),        # Estruturas de repetição
    ("REPEAT",        r'\brepeat\b'),            # palavra reservada "repeat"
    ("UNTIL",         r'\buntil\b'),             # palavra reservada "until"
    ("FOR_TO_DO",     r'\b(for|to|do)\b'),       # Estrutura de for-to-do
    ("OP_LOGICO",     r'\b(and|or|not)\b'),      # Operadores logicos
    ("OP",            r'\bmod\b|[+\-*/]'),       # Operadores
    ("OP_RELACIONAL", r'<=|>=|<>|<|>|='),        # Operadores relacionais
    ("ASSIGN",        r':='),                    # Atribuicao
    ("ID",            r'[A-Za-z_]\w*'),          # Identificadores
    ("DELIMITER",     r'[();,:]'),               # Simbolos especiais
    ("SKIP",          r'[ \t]+'),                # Espacos e tabulacoes
    ("MISMATCH",      r'.'),                     # Qualquer coisa inesperada
]

tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
# re.DOTALL faz com que o regex r'.' idendifique qualquer caractere mais o caractere de quebra de linha (\n),
# isso faz que ele consiga indentificar comentarios de multiplas linhas
get_token = re.compile(tok_regex, re.DOTALL).match

def lexer(code):
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f"Caractere inválido em {pos}")
        kind = match.lastgroup
        value = match.group()
        # Faz verificacao se o ID eh igual a algum token presente na lista "palvras_reservadas"
        if(kind == "ID" and value.upper() in palavras_reservadas):# O compilador vai ser case-sensitive?
            kind = "RESERVED_TOKEN"
        if kind not in ("SKIP", "MISMATCH", "COMMENT"):
            yield kind, value
        pos = match.end()

try:
    with open(arquivo_de_entrada, 'r', encoding='utf-8') as leitor:
        codigo_completo = leitor.read()
        tokens = list(lexer(codigo_completo))
    with open(arquivo_de_saida, 'w', encoding='utf-8') as escritor:
        for token in tokens:
            escritor.write(str(token) + "\n")
            # Se quiser printar no terminal...
            #print(token)
except FileNotFoundError:
    print(f"O arquivo nao foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
