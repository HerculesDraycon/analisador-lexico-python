# 🚀 Analisador Léxico - Interface Web

Uma interface web moderna, responsiva e funcional para o analisador léxico em Python, mantendo toda a lógica original do analisador.

## ✨ Características

- **Interface Responsiva**: Funciona perfeitamente em desktop, tablet e mobile
- **Design Moderno**: Interface limpa e agradável com gradientes e animações
- **Funcionalidades Completas**: 
  - Análise em tempo real do código Pascal
  - Contadores de linhas e caracteres
  - Exemplos pré-carregados
  - Download dos resultados
  - Legenda interativa de tokens
  - Atalhos de teclado

## 🛠️ Instalação e Execução

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
python app.py
```

### 3. Acessar a Interface
Abra seu navegador e acesse: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
analisador-lexico-python/
├── app.py                 # Servidor Flask principal
├── analisador.py         # Analisador léxico original
├── requirements.txt      # Dependências Python
├── templates/
│   └── index.html       # Interface HTML
├── static/
│   ├── css/
│   │   └── style.css    # Estilos CSS
│   └── js/
│       └── script.js    # JavaScript interativo
├── entrada.txt          # Arquivo de exemplo
├── exemplo.txt          # Arquivo de exemplo
└── README_INTERFACE.md  # Esta documentação
```

## 🎯 Como Usar

### 1. **Inserir Código**
- Digite ou cole seu código Pascal na área de texto
- Use o botão "Exemplo" para carregar um código de demonstração
- Use "Limpar" para apagar o conteúdo

### 2. **Analisar**
- Clique em "Analisar Código" ou use `Ctrl+Enter`
- Os tokens serão exibidos em tempo real
- Cada token é colorido por categoria

### 3. **Visualizar Resultados**
- Tokens organizados por tipo e valor
- Contador total de tokens
- Legenda explicativa das categorias

### 4. **Download**
- Clique em "Download" para salvar os resultados
- Arquivo `.txt` com análise completa

## ⌨️ Atalhos de Teclado

- `Ctrl+Enter`: Analisar código
- `Ctrl+L`: Limpar código
- `Ctrl+E`: Carregar exemplo
- `Tab`: Indentação no editor (4 espaços)

## 🎨 Tipos de Tokens Suportados

| Tipo | Descrição | Cor |
|------|-----------|-----|
| `RESERVED_TOKEN` | Palavras reservadas | Roxo/Azul |
| `ID` | Identificadores | Verde |
| `NUMBER` | Números | Laranja |
| `STRING/CHAR` | Strings e caracteres | Rosa |
| `OP*` | Operadores | Azul |
| `DELIMITER` | Delimitadores | Roxo |
| `CONDITIONAL` | Condicionais | Verde-água |
| `LOOP` | Estruturas de repetição | Rosa escuro |

## 🔧 Funcionalidades Técnicas

### Backend (Flask)
- Endpoint `/analyze` para análise de código
- Tratamento de erros robusto
- API RESTful com respostas JSON
- Integração completa com o analisador original

### Frontend
- Interface 100% responsiva
- Animações suaves e feedback visual
- Contadores em tempo real
- Modal de erros
- Loading states
- Toast notifications

### Responsividade
- **Desktop**: Layout em grid com sidebar
- **Tablet**: Layout adaptativo
- **Mobile**: Layout vertical otimizado

## 🚀 Melhorias Implementadas

1. **Interface Visual**
   - Design moderno com gradientes
   - Tipografia otimizada (Inter font)
   - Ícones Font Awesome
   - Animações CSS

2. **Experiência do Usuário**
   - Feedback visual imediato
   - Estados de loading
   - Tratamento de erros amigável
   - Atalhos de teclado

3. **Funcionalidades Extras**
   - Download de resultados
   - Exemplos pré-carregados
   - Contadores em tempo real
   - Cópia de tokens (clique)

## 🔍 Compatibilidade

- **Navegadores**: Chrome, Firefox, Safari, Edge (versões modernas)
- **Dispositivos**: Desktop, Tablet, Mobile
- **Python**: 3.7+
- **Flask**: 2.3+

## 📝 Notas Importantes

- O analisador léxico original (`analisador.py`) permanece intacto
- Toda a lógica de análise é preservada
- A interface é uma camada adicional, não substitui o original
- Suporte completo a todos os tokens do Pascal definidos

## 🎉 Pronto para Usar!

A interface está completamente funcional e pronta para demonstrações acadêmicas ou uso prático. Mantém toda a precisão do analisador original com uma experiência visual moderna e intuitiva.