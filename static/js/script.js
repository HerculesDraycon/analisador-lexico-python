// Elementos DOM
const codeInput = document.getElementById('codeInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const exampleBtn = document.getElementById('exampleBtn');
const downloadBtn = document.getElementById('downloadBtn');
const resultsContainer = document.getElementById('resultsContainer');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorModal = document.getElementById('errorModal');
const errorMessage = document.getElementById('errorMessage');
const lineCount = document.getElementById('lineCount');
const charCount = document.getElementById('charCount');
const tokenCount = document.getElementById('tokenCount');

// Estado da aplicação
let currentTokens = [];
let analysisResults = null;

// Código de exemplo
const exampleCode = `program teste;
var x, y: integer;
const pi := 3.1416;
begin
    read(x);
    if (x > 0) and (y < 10) then
        result := true or false;
    else
        result := not (x = y);
    
    while (x < 10) do
        x := x + 1;
    
    writeln("Resultado: ", result);
    write(x)
end`;

// Mapeamento de cores para tipos de token
const tokenColors = {
    'RESERVED_TOKEN': 'reserved',
    'ID': 'identifier',
    'NUMBER': 'number',
    'STRING': 'string',
    'CHAR': 'string',
    'OP': 'operator',
    'OP_LOGICO': 'operator',
    'OP_RELACIONAL': 'operator',
    'ASSIGN': 'operator',
    'DELIMITER': 'delimiter',
    'CONDITIONAL': 'conditional',
    'LOOP': 'loop',
    'REPEAT': 'loop',
    'UNTIL': 'loop',
    'FOR_TO_DO': 'loop',
    'BLOCK': 'conditional',
    'READ': 'conditional',
    'WRITE': 'conditional',
    'WRITELN': 'conditional'
};

// Variáveis globais
let currentFile = null;

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    updateCounters();
}

function setupEventListeners() {
    // Event listeners existentes
    const analyzeBtn = document.getElementById('analyzeBtn');
    const codeInput = document.getElementById('codeInput');
    
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeCode);
    }
    
    if (codeInput) {
        codeInput.addEventListener('input', updateCounters);
        codeInput.addEventListener('keydown', handleTabKey);
    }
    
    // Botões principais
    const clearBtn = document.getElementById('clearBtn');
    const exampleBtn = document.getElementById('exampleBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    
    if (clearBtn) {
        clearBtn.addEventListener('click', clearCode);
    }
    
    if (exampleBtn) {
        exampleBtn.addEventListener('click', loadExample);
    }
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadResults);
    }
    
    // Modal de erro
    const modalCloseButtons = document.querySelectorAll('.modal-close');
    modalCloseButtons.forEach(btn => {
        btn.addEventListener('click', closeErrorModal);
    });
    
    // Fechar modal clicando fora
    const errorModal = document.getElementById('errorModal');
    if (errorModal) {
        errorModal.addEventListener('click', function(e) {
            if (e.target === errorModal) {
                closeErrorModal();
            }
        });
    }
    
    // Atalhos de teclado
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Novos event listeners para upload de arquivos
    setupFileUpload();
}

function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    if (!uploadArea || !fileInput) return;
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File input change event
    fileInput.addEventListener('change', handleFileSelect);
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Verificar tipo de arquivo
    const allowedTypes = ['text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const allowedExtensions = ['.txt', '.docx'];
    
    const fileName = file.name.toLowerCase();
    const isValidType = allowedTypes.includes(file.type) || 
                       allowedExtensions.some(ext => fileName.endsWith(ext));
    
    if (!isValidType) {
        showError('Tipo de arquivo não suportado. Use apenas arquivos .txt ou .docx');
        return;
    }
    
    // Verificar tamanho do arquivo (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('Arquivo muito grande. Tamanho máximo: 16MB');
        return;
    }
    
    currentFile = file;
    showFileInfo(file);
    uploadAndAnalyzeFile(file);
}

function showFileInfo(file) {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    
    if (fileInfo && fileName && fileSize) {
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';
    }
}

function removeFile() {
    currentFile = null;
    const fileInfo = document.getElementById('fileInfo');
    const fileInput = document.getElementById('fileInput');
    
    if (fileInfo) fileInfo.style.display = 'none';
    if (fileInput) fileInput.value = '';
    
    // Limpar textarea
    const codeInput = document.getElementById('codeInput');
    if (codeInput) {
        codeInput.value = '';
        updateCounters();
    }
    
    // Limpar resultados
    clearCode();
}

function uploadAndAnalyzeFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Mostrar loading
    showLoading(true);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        
        if (data.success) {
            // Preencher textarea com o conteúdo extraído
            const codeInput = document.getElementById('codeInput');
            if (codeInput) {
                codeInput.value = data.content;
                updateCounters();
            }
            
            // Exibir resultados da análise
            if (data.tokens) {
                currentTokens = data.tokens;
                analysisResults = data;
                displayResults(data.tokens);
            }
            
            showSuccess(`Arquivo "${data.filename}" analisado com sucesso!`);
        } else {
            showError(data.error || 'Erro ao processar arquivo');
        }
    })
    .catch(error => {
        showLoading(false);
        console.error('Erro:', error);
        showError('Erro ao enviar arquivo para o servidor');
    });
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Atualizar contadores
function updateCounters() {
    const text = codeInput.value;
    const lines = text.split('\n').length;
    const chars = text.length;
    
    if (lineCount) lineCount.textContent = `Linhas: ${lines}`;
    if (charCount) charCount.textContent = `Caracteres: ${chars}`;
}

// Manipular tecla Tab no textarea
function handleTabKey(e) {
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = codeInput.selectionStart;
        const end = codeInput.selectionEnd;
        const value = codeInput.value;
        
        codeInput.value = value.substring(0, start) + '    ' + value.substring(end);
        codeInput.selectionStart = codeInput.selectionEnd = start + 4;
    }
}

// Atalhos de teclado
function handleKeyboardShortcuts(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'Enter':
                e.preventDefault();
                analyzeCode();
                break;
            case 'l':
                e.preventDefault();
                clearCode();
                break;
            case 'e':
                e.preventDefault();
                loadExample();
                break;
        }
    }
}

// Analisar código
async function analyzeCode() {
    const code = codeInput.value.trim();
    
    if (!code) {
        showError('Por favor, digite algum código para analisar.');
        return;
    }
    
    showLoading(true);
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro na análise do código');
        }
        
        currentTokens = data.tokens;
        analysisResults = data;
        displayResults(data.tokens);
        
    } catch (error) {
        console.error('Erro na análise:', error);
        showError(`Erro na análise: ${error.message}`);
    } finally {
        showLoading(false);
        analyzeBtn.disabled = false;
    }
}

// Exibir resultados
function displayResults(tokens) {
    if (!tokens || tokens.length === 0) {
        showEmptyResults();
        return;
    }
    
    const tokensGrid = document.createElement('div');
    tokensGrid.className = 'tokens-grid';
    
    tokens.forEach((token, index) => {
        const tokenItem = createTokenElement(token, index);
        tokensGrid.appendChild(tokenItem);
    });
    
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(tokensGrid);
    
    // Atualizar contador de tokens
    tokenCount.textContent = `${tokens.length} tokens`;
    downloadBtn.style.display = 'inline-flex';
    
    // Scroll suave para os resultados
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Criar elemento de token
function createTokenElement(token, index) {
    const [type, value] = token;
    const tokenItem = document.createElement('div');
    tokenItem.className = 'token-item';
    
    const colorClass = tokenColors[type] || 'default';
    
    tokenItem.innerHTML = `
        <span class="token-badge ${colorClass}">${type}</span>
        <span class="token-value">${escapeHtml(value)}</span>
    `;
    
    // Animação de entrada
    tokenItem.style.animationDelay = `${index * 0.05}s`;
    
    return tokenItem;
}

// Exibir estado vazio
function showEmptyResults() {
    resultsContainer.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-search"></i>
            <p>Nenhum token encontrado</p>
            <small>O código analisado não contém tokens válidos</small>
        </div>
    `;
    tokenCount.textContent = '0 tokens';
    downloadBtn.style.display = 'none';
}

// Limpar código
function clearCode() {
    if (codeInput.value.trim() && !confirm('Tem certeza que deseja limpar o código?')) {
        return;
    }
    
    codeInput.value = '';
    updateCounters();
    codeInput.focus();
    
    // Limpar resultados
    resultsContainer.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-search"></i>
            <p>Nenhuma análise realizada ainda</p>
            <small>Digite um código e clique em "Analisar Código" para ver os tokens</small>
        </div>
    `;
    tokenCount.textContent = '0 tokens';
    downloadBtn.style.display = 'none';
    currentTokens = [];
    analysisResults = null;
}

// Carregar exemplo
function loadExample() {
    if (codeInput.value.trim() && !confirm('Isso substituirá o código atual. Continuar?')) {
        return;
    }
    
    codeInput.value = exampleCode;
    updateCounters();
    codeInput.focus();
    
    // Animação de digitação
    animateTyping();
}

// Animação de digitação
function animateTyping() {
    const originalValue = codeInput.value;
    codeInput.value = '';
    
    let i = 0;
    const typeInterval = setInterval(() => {
        if (i < originalValue.length) {
            codeInput.value += originalValue.charAt(i);
            i++;
            updateCounters();
        } else {
            clearInterval(typeInterval);
        }
    }, 20);
}

// Download dos resultados
function downloadResults() {
    if (!currentTokens || currentTokens.length === 0) {
        showError('Nenhum resultado para download.');
        return;
    }
    
    try {
        let content = 'ANÁLISE LÉXICA - RESULTADOS\n';
        content += '=' .repeat(50) + '\n\n';
        content += `Data: ${new Date().toLocaleString('pt-BR')}\n`;
        content += `Total de tokens: ${currentTokens.length}\n\n`;
        content += 'TOKENS IDENTIFICADOS:\n';
        content += '-'.repeat(30) + '\n';
        
        currentTokens.forEach((token, index) => {
            const [type, value] = token;
            content += `${(index + 1).toString().padStart(3, '0')}. ${type.padEnd(15)} | ${value}\n`;
        });
        
        content += '\n' + '='.repeat(50) + '\n';
        content += 'Gerado pelo Analisador Léxico Web\n';
        
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analise_lexica_${new Date().toISOString().slice(0, 10)}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        // Feedback visual
        const originalText = downloadBtn.innerHTML;
        downloadBtn.innerHTML = '<i class="fas fa-check"></i> Baixado!';
        downloadBtn.style.background = 'var(--success-color)';
        
        setTimeout(() => {
            downloadBtn.innerHTML = originalText;
            downloadBtn.style.background = '';
        }, 2000);
        
    } catch (error) {
        console.error('Erro no download:', error);
        showError('Erro ao gerar arquivo de download.');
    }
}

// Exibir loading
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// Exibir erro
function showError(message) {
    errorMessage.textContent = message;
    errorModal.style.display = 'flex';
}

// Fechar modal de erro
function closeErrorModal() {
    errorModal.style.display = 'none';
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Utilitários para feedback visual
function showSuccess(message) {
    // Criar toast de sucesso
    const toast = document.createElement('div');
    toast.className = 'toast toast-success';
    toast.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Remover após 3 segundos
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Adicionar estilos para toast (se necessário)
const toastStyles = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1002;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease-out;
    }
    
    .toast-success {
        background: var(--success-color);
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;

// Adicionar estilos ao head se não existirem
if (!document.querySelector('#toast-styles')) {
    const style = document.createElement('style');
    style.id = 'toast-styles';
    style.textContent = toastStyles;
    document.head.appendChild(style);
}

// Função para copiar token para clipboard
function copyToken(token) {
    const [type, value] = token;
    const text = `${type}: ${value}`;
    
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Token copiado para a área de transferência!');
    }).catch(() => {
        // Fallback para navegadores mais antigos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showSuccess('Token copiado para a área de transferência!');
    });
}

// Adicionar funcionalidade de cópia aos tokens (será chamada quando os tokens forem criados)
function addCopyFunctionality() {
    const tokenItems = document.querySelectorAll('.token-item');
    tokenItems.forEach((item, index) => {
        item.style.cursor = 'pointer';
        item.title = 'Clique para copiar';
        item.addEventListener('click', () => {
            if (currentTokens[index]) {
                copyToken(currentTokens[index]);
            }
        });
    });
}

// Modificar a função displayResults para incluir funcionalidade de cópia
const originalDisplayResults = displayResults;
displayResults = function(tokens) {
    originalDisplayResults(tokens);
    // Adicionar funcionalidade de cópia após um pequeno delay para garantir que os elementos foram criados
    setTimeout(addCopyFunctionality, 100);
};