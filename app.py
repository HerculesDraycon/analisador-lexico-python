import re
import sys

# ==============================================================================
# 1. ANALISADOR LÉXICO (Mantido, mas gera tokens para o parser)
# ==============================================================================

palavras_reservadas = {
    "PROGRAM", "VAR", "INTEGER", "BOOLEAN", "BEGIN", "END", "IF", "THEN",
    "ELSE", "WHILE", "DO", "READ", "READLN", "WRITE", "WRITELN", "TRUE", "FALSE"
}

token_specification = [
    ("COMMENT",       r'/\*.*?\*/'),                    
    ("STRING",        r"'[^']*'"),                      
    ("NUMBER",        r'\d+(\.\d*)?'),                  
    ("ASSIGN",        r':='),                           
    ("LE_EQ",         r'<='),                           
    ("GE_EQ",         r'>='),                           
    ("NE_EQ",         r'<>'),                           
    ("SEMI",          r';'),
    ("COLON",         r':'),
    ("COMMA",         r','),
    ("DOT",           r'\.'),                           
    ("LPAREN",        r'\('),
    ("RPAREN",        r'\)'),
    ("PLUS",          r'\+'),
    ("MINUS",         r'-'),
    ("TIMES",         r'\*'),
    ("DIVIDE",        r'/'),
    ("EQUAL",         r'='),
    ("LESS",          r'<'),
    ("GREATER",       r'>'),
    ("ID",            r'[A-Za-z_]\w*'),                 
    ("SKIP",          r'[ \t\n]+'),                     
    ("MISMATCH",      r'.'),                            
]

tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
get_token = re.compile(tok_regex, re.DOTALL).match

def lexer(code):
    line_num = 1
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f"Caractere inválido na posição {pos}")
        
        kind = match.lastgroup
        value = match.group()
        
        if kind == "SKIP":
            line_num += value.count('\n')
        elif kind == "ID":
            if value.upper() in palavras_reservadas:
                kind = value.upper() 
            yield kind, value, line_num
        elif kind == "MISMATCH":
            raise SyntaxError(f"Erro léxico: '{value}' na linha {line_num}")
        elif kind != "COMMENT":
            yield kind, value, line_num
            
        pos = match.end()
    
    yield "EOF", "", line_num

# ==============================================================================
# 2. ANALISADOR SINTÁTICO COM LOGS (Instrumentado)
# ==============================================================================

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.indent_level = 0 # Controla a indentação dos logs

    # --- Helpers de Log ---
    def _log(self, msg):
        indent = "|   " * self.indent_level
        print(f"{indent}{msg}")

    def _enter_rule(self, rule_name):
        self._log(f"┌── ENTER <{rule_name}>")
        self.indent_level += 1

    def _exit_rule(self, rule_name):
        self.indent_level -= 1
        self._log(f"└── REDUCE <{rule_name}> (Regra validada)")

    def _shift_log(self, token_type, value):
        indent = "|   " * self.indent_level
        print(f"{indent}>> SHIFT: Consumiu '{value}' ({token_type})")

    # --- Controle de Fluxo ---
    def error(self, msg):
        token_atual = self.current_token
        raise SyntaxError(
            f"\n[ERRO SINTÁTICO] {msg}\n"
            f"Linha: {token_atual[2]} | Encontrado: '{token_atual[1]}' ({token_atual[0]})"
        )

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self._shift_log(token_type, self.current_token[1])
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.error(f"Esperava token '{token_type}'")

    # --- Regras da Gramática (Métodos) ---

    def parse_program(self):
        self._enter_rule("programa")
        try:
            self.eat('PROGRAM')
            self.eat('ID')
            self.eat('SEMI')
            
            if self.current_token[0] == 'VAR':
                self.parse_declaracoes()
                
            self.eat('BEGIN')
            self.parse_lista_comandos()
            self.eat('END')
            self.eat('DOT')
        finally:
            self._exit_rule("programa")

    def parse_declaracoes(self):
        self._enter_rule("declarações")
        try:
            self.eat('VAR')
            while self.current_token[0] == 'ID':
                self.parse_lista_ids()
                self.eat('COLON')
                self.parse_tipo()
                self.eat('SEMI')
        finally:
            self._exit_rule("declarações")

    def parse_lista_ids(self):
        self._enter_rule("lista_ids")
        try:
            self.eat('ID')
            while self.current_token[0] == 'COMMA':
                self.eat('COMMA')
                self.eat('ID')
        finally:
            self._exit_rule("lista_ids")

    def parse_tipo(self):
        self._enter_rule("tipo")
        try:
            if self.current_token[0] in ('INTEGER', 'BOOLEAN'):
                self.eat(self.current_token[0])
            else:
                self.error("Esperado tipo 'integer' ou 'boolean'")
        finally:
            self._exit_rule("tipo")

    def parse_lista_comandos(self):
        self._enter_rule("lista_comandos")
        try:
            self.parse_comando()
            self.eat('SEMI')
            
            first_comando = {'ID', 'READ', 'READLN', 'WRITE', 'WRITELN', 'BEGIN', 'IF', 'WHILE'}
            while self.current_token[0] in first_comando:
                self.parse_comando()
                self.eat('SEMI')
        finally:
            self._exit_rule("lista_comandos")

    def parse_comando(self):
        self._enter_rule("comando")
        try:
            token_type = self.current_token[0]
            if token_type == 'ID':
                self.parse_atribuicao()
            elif token_type in ('READ', 'READLN'):
                self.parse_leitura()
            elif token_type in ('WRITE', 'WRITELN'):
                self.parse_escrita()
            elif token_type == 'BEGIN':
                self.parse_composto()
            elif token_type == 'IF':
                self.parse_condicional()
            elif token_type == 'WHILE':
                self.parse_repeticao()
            else:
                self.error("Comando não reconhecido")
        finally:
            self._exit_rule("comando")

    def parse_atribuicao(self):
        self._enter_rule("atribuição")
        try:
            self.eat('ID')
            self.eat('ASSIGN')
            self.parse_expr()
        finally:
            self._exit_rule("atribuição")

    def parse_leitura(self):
        self._enter_rule("leitura")
        try:
            if self.current_token[0] == 'READ':
                self.eat('READ')
                self.eat('LPAREN')
                self.parse_lista_ids()
                self.eat('RPAREN')
            elif self.current_token[0] == 'READLN':
                self.eat('READLN')
                if self.current_token[0] == 'LPAREN':
                    self.eat('LPAREN')
                    self.parse_lista_ids()
                    self.eat('RPAREN')
        finally:
            self._exit_rule("leitura")

    def parse_escrita(self):
        self._enter_rule("escrita")
        cmd = self.current_token[0]
        try:
            self.eat(cmd)
            if self.current_token[0] == 'LPAREN':
                self.eat('LPAREN')
                self.parse_lista_stringvar()
                self.eat('RPAREN')
        finally:
            self._exit_rule("escrita")

    def parse_lista_stringvar(self):
        self._enter_rule("lista_stringvar")
        try:
            self.parse_stringvar()
            while self.current_token[0] == 'COMMA':
                self.eat('COMMA')
                self.parse_stringvar()
        finally:
            self._exit_rule("lista_stringvar")

    def parse_stringvar(self):
        # Não logaremos enter/exit aqui para não poluir muito, pois é muito simples
        if self.current_token[0] == 'STRING':
            self.eat('STRING')
        else:
            self.parse_expr()

    def parse_composto(self):
        self._enter_rule("composto")
        try:
            self.eat('BEGIN')
            self.parse_lista_comandos()
            self.eat('END')
        finally:
            self._exit_rule("composto")

    def parse_condicional(self):
        self._enter_rule("condicional")
        try:
            self.eat('IF')
            self.parse_exprboolean()
            self.eat('THEN')
            self.parse_comando()
            if self.current_token[0] == 'ELSE':
                self.eat('ELSE')
                self.parse_comando()
        finally:
            self._exit_rule("condicional")

    def parse_repeticao(self):
        self._enter_rule("repetição")
        try:
            self.eat('WHILE')
            self.parse_exprboolean()
            self.eat('DO')
            self.parse_comando()
        finally:
            self._exit_rule("repetição")

    def parse_exprboolean(self):
        self._enter_rule("expr_boolean")
        try:
            self.parse_expr()
            ops_relacionais = {'LESS', 'LE_EQ', 'GREATER', 'GE_EQ', 'EQUAL', 'NE_EQ'}
            if self.current_token[0] in ops_relacionais:
                self.eat(self.current_token[0])
                self.parse_expr()
        finally:
            self._exit_rule("expr_boolean")

    def parse_expr(self):
        self._enter_rule("expressão")
        try:
            self.parse_termo()
            while self.current_token[0] in ('PLUS', 'MINUS'):
                self.eat(self.current_token[0])
                self.parse_termo()
        finally:
            self._exit_rule("expressão")

    def parse_termo(self):
        self._enter_rule("termo")
        try:
            self.parse_fator()
            while self.current_token[0] in ('TIMES', 'DIVIDE'):
                self.eat(self.current_token[0])
                self.parse_fator()
        finally:
            self._exit_rule("termo")

    def parse_fator(self):
        self._enter_rule("fator")
        try:
            token = self.current_token
            if token[0] in ('PLUS', 'MINUS'):
                self.eat(token[0])
                self.parse_fator()
            elif token[0] == 'LPAREN':
                self.eat('LPAREN')
                self.parse_expr()
                self.eat('RPAREN')
            elif token[0] == 'ID':
                self.eat('ID')
            elif token[0] == 'NUMBER':
                self.eat('NUMBER')
            else:
                self.error("Fator inesperado")
        finally:
            self._exit_rule("fator")

# ==============================================================================
# 3. EXECUÇÃO
# ==============================================================================

if __name__ == "__main__":
    print("Digite o nome do arquivo que deseja ler: ")
    nome_arquivo = input()

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            codigo = file.read()
        
        print("\n" + "="*40)
        print("INICIANDO ANÁLISE SINTÁTICA DETALHADA")
        print("Legenda: ENTER = Prevendo Regra | SHIFT = Consumindo Token | REDUCE = Regra Reconhecida")
        print("="*40 + "\n")
        
        tokens_gerados = list(lexer(codigo))
        
        parser = Parser(tokens_gerados)
        parser.parse_program()
        
        print("\n" + "="*40)
        print("RESULTADO: O CÓDIGO FONTE É VÁLIDO.")
        print("="*40)
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except SyntaxError as e:
        print(f"\n[FALHA NA ANÁLISE] O código é INVÁLIDO.")
        print(e)
    except Exception as e:
        print(f"\nErro inesperado: {e}")