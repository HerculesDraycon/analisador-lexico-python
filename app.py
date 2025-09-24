from flask import Flask, render_template, request, jsonify
import os
import re
import traceback
from docx import Document
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Criar pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Extensões de arquivo permitidas
ALLOWED_EXTENSIONS = {'txt', 'docx'}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path, filename):
    """Extrai texto de arquivos .txt ou .docx"""
    try:
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'txt':
            # Ler arquivo .txt
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        elif file_extension == 'docx':
            # Ler arquivo .docx
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        
        else:
            return None
            
    except Exception as e:
        print(f"Erro ao extrair texto do arquivo: {e}")
        return None
palavras_reservadas = {
    "ABSOLUTE", "AND", "ARRAY", "BEGIN", "CASE", "CHAR", "CONST", "DIV", "DO",
    "DOWNTO", "ELSE", "END", "EXTERNAL", "FILE", "FOR", "FORWARD", "FUNC",
    "FUNCTION", "GOTO", "IF", "IMPLEMENTATION", "INTEGER", "INTERFACE",
    "INTERRUPT", "LABEL", "MAIN", "NIL", "NIT", "NOT", "OF", "OR", "PACKED",
    "PROC", "PROGRAM", "REAL", "RECORD", "REPEAT", "SET", "SHL", "SHR",
    "STRING", "THEN", "TO", "TYPE", "UNIT", "UNTIL", "USES", "VAR",
    "WHILE", "WITH", "XOR"
}

# Definição dos padrões de tokens (copiado do analisador original)
token_specification = [
    ("COMMENT",       r'/\*.*?\*/'),             # Comentarios
    ("READ",          r'\bread\b'),              # Comando de entrada
    ("WRITE",         r'\bwrite\b'),             # Comando de saída
    ("WRITELN",       r'\bwriteln\b'),           # Comando de saída com quebra de linha
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

# Compilar regex (copiado do analisador original)
tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
get_token = re.compile(tok_regex, re.DOTALL).match

def lexer(code):
    """
    Função lexer original adaptada para retornar lista de tokens
    """
    tokens = []
    pos = 0
    
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f"Caractere inválido na posição {pos}: '{code[pos]}'")
        
        kind = match.lastgroup
        value = match.group()
        
        # Verificação se o ID é igual a algum token presente na lista "palavras_reservadas"
        if kind == "ID" and value.upper() in palavras_reservadas:
            kind = "RESERVED_TOKEN"
        
        # Filtrar tokens desnecessários
        if kind not in ("SKIP", "MISMATCH", "COMMENT"):
            tokens.append((kind, value))
        
        pos = match.end()
    
    return tokens

@app.route('/')
def index():
    """Rota principal que serve a interface web"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Endpoint para análise do código
    Recebe código via POST e retorna tokens em JSON
    """
    try:
        # Obter dados da requisição
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'error': 'Código não fornecido',
                'details': 'O campo "code" é obrigatório'
            }), 400
        
        code = data['code'].strip()
        
        if not code:
            return jsonify({
                'error': 'Código vazio',
                'details': 'Por favor, forneça algum código para análise'
            }), 400
        
        # Executar análise léxica
        tokens = lexer(code)
        
        # Estatísticas
        token_types = {}
        for token_type, _ in tokens:
            token_types[token_type] = token_types.get(token_type, 0) + 1
        
        # Resposta de sucesso
        return jsonify({
            'success': True,
            'tokens': tokens,
            'total_tokens': len(tokens),
            'token_types': token_types,
            'code_length': len(code),
            'code_lines': len(code.split('\n'))
        })
        
    except SyntaxError as e:
        # Erro de sintaxe no código
        return jsonify({
            'error': 'Erro de sintaxe',
            'details': str(e)
        }), 400
        
    except Exception as e:
        # Erro interno do servidor
        app.logger.error(f"Erro na análise: {str(e)}")
        app.logger.error(traceback.format_exc())
        
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': 'Ocorreu um erro inesperado durante a análise'
        }), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Rota para upload e análise de arquivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            # Salvar arquivo com nome seguro
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extrair texto do arquivo
            text_content = extract_text_from_file(file_path, filename)
            
            # Remover arquivo após extração
            os.remove(file_path)
            
            if text_content is None:
                return jsonify({'error': 'Erro ao extrair texto do arquivo'}), 500
            
            # Analisar o texto extraído
            tokens = lexer(text_content)
            
            # Estatísticas
            token_types = {}
            for token_type, _ in tokens:
                token_types[token_type] = token_types.get(token_type, 0) + 1
            
            return jsonify({
                'success': True,
                'filename': filename,
                'content': text_content,
                'tokens': tokens,
                'total_tokens': len(tokens),
                'token_types': token_types
            })
        
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido. Use apenas .txt ou .docx'}), 400
    
    except Exception as e:
        print(f"Erro no upload: {e}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Endpoint para verificação de saúde da aplicação"""
    return jsonify({
        'status': 'healthy',
        'service': 'Analisador Léxico Web',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handler para páginas não encontradas"""
    return jsonify({
        'error': 'Página não encontrada',
        'details': 'O recurso solicitado não existe'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erros internos do servidor"""
    return jsonify({
        'error': 'Erro interno do servidor',
        'details': 'Ocorreu um erro inesperado'
    }), 500

# Configurações de desenvolvimento
if __name__ == '__main__':
    # Verificar se as pastas necessárias existem
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Configurações de debug
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    print("=" * 60)
    print("🚀 ANALISADOR LÉXICO - INTERFACE WEB")
    print("=" * 60)
    print("📁 Estrutura de arquivos:")
    print("   ├── app.py (servidor Flask)")
    print("   ├── templates/")
    print("   │   └── index.html")
    print("   └── static/")
    print("       ├── css/style.css")
    print("       └── js/script.js")
    print()
    print("🌐 Servidor iniciando em: http://localhost:5000")
    print("📝 Baseado no analisador léxico Python original")
    print("=" * 60)
    
    # Iniciar servidor
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )