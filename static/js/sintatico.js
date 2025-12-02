document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.getElementById('codeInput');
    const parseBtn = document.getElementById('parseBtn');
    const resultsContainer = document.getElementById('resultsContainerSintatico');
    const statusSintatico = document.getElementById('statusSintatico');
    const downloadBtn = document.getElementById('downloadBtnSintatico');
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');

    function showLoading(show) {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) loadingOverlay.style.display = show ? 'flex' : 'none';
    }

    function showError(message) {
        if (errorMessage && errorModal) {
            errorMessage.textContent = message;
            errorModal.style.display = 'flex';
        }
    }

    function closeErrorModal() {
        if (errorModal) errorModal.style.display = 'none';
    }
    document.querySelectorAll('.modal-close').forEach(btn => btn.addEventListener('click', closeErrorModal));

    // Upload área
    const uploadArea = document.getElementById('uploadAreaSintatico');
    const fileInput = document.getElementById('fileInputSintatico');
    const fileInfo = document.getElementById('fileInfoSintatico');
    const fileName = document.getElementById('fileNameSintatico');
    const fileSize = document.getElementById('fileSizeSintatico');

    if (uploadArea && fileInput) {
        uploadArea.addEventListener('dragover', e => { e.preventDefault(); uploadArea.classList.add('dragover'); });
        uploadArea.addEventListener('dragleave', e => { e.preventDefault(); uploadArea.classList.remove('dragover'); });
        uploadArea.addEventListener('drop', e => {
            e.preventDefault(); uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files; if (files.length > 0) handleFile(files[0]);
        });
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', e => { const files = e.target.files; if (files.length > 0) handleFile(files[0]); });
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024; const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function handleFile(file) {
        const allowedTypes = ['text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        const allowedExtensions = ['.txt', '.docx'];
        const fileNameLower = file.name.toLowerCase();
        const isValidType = allowedTypes.includes(file.type) || allowedExtensions.some(ext => fileNameLower.endsWith(ext));
        if (!isValidType) { showError('Tipo de arquivo não suportado. Use .txt ou .docx'); return; }
        if (file.size > 16 * 1024 * 1024) { showError('Arquivo muito grande. Máximo: 16MB'); return; }
        if (fileInfo && fileName && fileSize) {
            fileName.textContent = file.name; fileSize.textContent = formatFileSize(file.size); fileInfo.style.display = 'block';
        }
        uploadAndParseFile(file);
    }

    function removeFileSintatico() {
        if (fileInfo) fileInfo.style.display = 'none'; if (fileInput) fileInput.value = '';
        if (codeInput) codeInput.value = '';
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <p>Nenhuma análise realizada ainda</p>
                <small>Digite um código e clique em "Validar Sintaxe" para ver os logs</small>
            </div>
        `;
        statusSintatico.textContent = 'Aguardando análise';
        downloadBtn.style.display = 'none';
    }

    function renderLogs(logs) {
        const pre = document.createElement('pre');
        pre.style.whiteSpace = 'pre-wrap';
        pre.style.fontFamily = 'Fira Code, Consolas, Monaco, monospace';
        pre.style.background = 'var(--bg-secondary)';
        pre.style.border = '1px solid var(--border-color)';
        pre.style.borderRadius = '6px';
        pre.style.padding = '16px';
        pre.textContent = logs.join('\n');
        resultsContainer.innerHTML = '';
        resultsContainer.appendChild(pre);
    }

    async function parseCode(code) {
        showLoading(true); parseBtn.disabled = true;
        try {
            const response = await fetch('/parse', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Erro na análise sintática');
            renderLogs(data.logs || []);
            statusSintatico.textContent = data.valid ? 'Código válido' : 'Código inválido';
            downloadBtn.style.display = 'inline-flex';
            downloadBtn.onclick = () => downloadResults(data);
        } catch (err) {
            console.error(err); showError(err.message);
        } finally { showLoading(false); parseBtn.disabled = false; }
    }

    function downloadResults(data) {
        let content = 'ANÁLISE SINTÁTICA - LOGS\n';
        content += '='.repeat(50) + '\n\n';
        content += `Data: ${new Date().toLocaleString('pt-BR')}\n`;
        content += `Status: ${data.valid ? 'VÁLIDO' : 'INVÁLIDO'}\n`;
        content += '\nLOGS:\n' + (data.logs || []).join('\n') + '\n';
        const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url; a.download = 'analise_sintatica.txt';
        document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
    }

    async function uploadAndParseFile(file) {
        const formData = new FormData(); formData.append('file', file);
        showLoading(true);
        try {
            const response = await fetch('/upload_parse', { method: 'POST', body: formData });
            const data = await response.json();
            if (!response.ok || !data.success) throw new Error(data.error || 'Erro ao processar arquivo');
            if (codeInput) codeInput.value = data.content || '';
            renderLogs(data.logs || []);
            statusSintatico.textContent = data.valid ? 'Código válido' : 'Código inválido';
            downloadBtn.style.display = 'inline-flex';
            downloadBtn.onclick = () => downloadResults(data);
        } catch (err) { console.error(err); showError(err.message); }
        finally { showLoading(false); }
    }

    const exampleBtn = document.getElementById('exampleBtnSintatico');
    if (exampleBtn) {
        exampleBtn.addEventListener('click', () => {
            const example = `program exemplo;\nvar x: integer;\nbegin\n    x := (2 + 3) * 4;\n    if x >= 10 then\n        write(x);\n    else\n        writeln('menor que 10');\nend.`;
            if (codeInput) codeInput.value = example;
        });
    }

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

    if (codeInput) codeInput.addEventListener('keydown', handleTabKey);

    if (parseBtn) parseBtn.addEventListener('click', () => {
        const code = (codeInput?.value || '').trim();
        if (!code) { showError('Por favor, digite algum código para analisar.'); return; }
        parseCode(code);
    });
});
