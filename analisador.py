import re

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
    ("COMMENT",       r'/\*.*?\*/'),                    # Comentarios
    ("READ",          r'\bread\b'),                     # Comando de entrada
    ("WRITE",         r'\bwrite\b'),                    # Comando de saída
    ("WRITELN",       r'\bwriteln\b'),                  # Comando de saída com quebra de linha
    ("STRING",        r'"[^"]*"'),                      # Strings delimitadas por aspas duplas
    ("CHAR",          r"'[^']*'"),                      # Caracteres delimitados por aspas simples
    ("NUMBER",        r'\d+(\.\d*)?([eE][+-]?\d+)?'),   # Numeros inteiros, decimais e com notacao cientifica
    ("BEGIN",         r'\bbegin\b'),                    # Blocos de comandos
    ("END",           r'\bend\b'),                      # Blocos de comandos
    ("IF",            r'\bif\b'),                       # Condicionais
    ("THEN",          r'\bthen\b'),                     # Condicionais
    ("ELSE",          r'\belse\b'),                     # Condicionais
    ("WHILE",         r'\bwhile\b'),                    # Estruturas de repetição
    ("DO",            r'\bdo\b'),                       # Estruturas de repetição
    ("REPEAT",        r'\brepeat\b'),                   # palavra reservada "repeat"
    ("UNTIL",         r'\buntil\b'),                    # palavra reservada "until"
    ("FOR",           r'\bfor\b'),                      # Estrutura de for-to-do
    ("TO",            r'\bto\b'),                       # Estrutura de for-to-do
    ("AND",           r'\band\b'),                      # Operadores logicos
    ("OR",            r'\bor\b'),                       # Operadores logicos
    ("NOT",           r'\bnot\b'),                      # Operadores logicos
    ("MOD",           r'\bmod\b'),                      # Operadores
    ("DIV",           r'\bdiv\b'),                      # Operadores
    ("PLUS",          r'\+'),                       # Operadores
    ("MINUS",         r'-'),                     # Operadores
    ("DIVIDE",        r'/'),                              # Operadores
    ("TIMES",         r'\*'),                  # Operadores
    ("LESS_EQUAL",    r'<='),                        # Operadores relacionais
    ("GREATER_EQUAL", r'>='),                           # Operadores relacionais
    ("NOT_EQUAL",     r'<>'),                          # Operadores relacionais
    ("LESS_THAN",     r'<'),                         # Operadores relacionais
    ("GREATER_THAN",  r'>'),                           # Operadores relacionais
    ("EQUAL",         r'='),                              # Operadores relacionais
    ("ASSIGN",        r':='),                           # Atribuicao
    ("ID",            r'[A-Za-z_]\w*'),                 # Identificadores("LPAREN",  r"\("),
    ("LPAREN",        r'\('),
    ("RPAREN",        r'\)'),
    ("SEMI",          r';'),
    ("COLON",         r':'),
    ("COMMA",         r','),
    ("END_PROGRAM",   r'\.'),                           # Final de programa
    ("SKIP",          r'[ \t]+'),                       # Espacos e tabulacoes
    ("MISMATCH",      r'.'),                            # Qualquer coisa inesperada
]

tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
# re.DOTALL faz com que o regex r'.' idendifique qualquer caractere mais o caractere de quebra de linha (\n),
# isso faz que ele consiga indentificar comentarios de multiplas linhas
get_token = re.compile(tok_regex, re.DOTALL).match

print("Digite o nome do arquivo que deseja ler: ")
arquivo_de_entrada = input()
arquivo_de_saida = arquivo_de_entrada[:5] + "_output.txt"

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
