// ─── FileForge Web ───────────────────────────────────────────────

class FileForgeWeb {
    constructor() {
        this.files = [];
        this.convertedFiles = [];

        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.fileListContainer = document.getElementById('fileListContainer');
        this.fileCount = document.getElementById('fileCount');
        this.formatSelect = document.getElementById('formatSelect');
        this.qualityRange = document.getElementById('qualityRange');
        this.qualityValue = document.getElementById('qualityValue');
        this.convertBtn = document.getElementById('convertBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.resultsSection = document.getElementById('resultsSection');
        this.resultsContainer = document.getElementById('resultsContainer');
        this.resultTitle = document.getElementById('resultTitle');

        this.init();
    }

    init() {
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            this.addFiles(Array.from(e.dataTransfer.files));
        });

        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', () => {
            this.addFiles(Array.from(this.fileInput.files));
            this.fileInput.value = '';
        });

        this.qualityRange.addEventListener('input', () => {
            this.qualityValue.textContent = this.qualityRange.value + '%';
        });

        this.convertBtn.addEventListener('click', () => this.convertFiles());
        this.clearBtn.addEventListener('click', () => this.clearAll());
    }

    addFiles(newFiles) {
        for (const file of newFiles) {
            if (!this.files.some(f => f.name === file.name && f.size === file.size)) {
                this.files.push(file);
            }
        }
        this.render();
    }

    removeFile(index) {
        this.files.splice(index, 1);
        this.render();
    }

    clearAll() {
        this.files = [];
        this.convertedFiles = [];
        this.resultsSection.hidden = true;
        this.resultsContainer.innerHTML = '';
        this.render();
    }

    render() {
        this.fileCount.textContent = this.files.length;
        this.convertBtn.disabled = this.files.length === 0;

        if (this.files.length === 0) {
            this.fileListContainer.innerHTML = '<p class="empty-message">nenhum arquivo selecionado</p>';
            return;
        }

        let html = '';
        for (let i = 0; i < this.files.length; i++) {
            const f = this.files[i];
            const icon = f.type.startsWith('image/') ? '🖼️' :
                         f.type === 'text/plain' ? '📄' :
                         f.type === 'application/pdf' ? '📕' : '📎';
            const size = f.size < 1024 ? f.size + ' B' :
                         f.size < 1048576 ? (f.size / 1024).toFixed(1) + ' KB' :
                         (f.size / 1048576).toFixed(1) + ' MB';
            const type = f.type.split('/')[1] || f.name.split('.').pop() || '?';

            html += `
                <div class="file-item">
                    <div class="file-info">
                        <span class="icon">${icon}</span>
                        <span class="name">${this.escape(f.name)}</span>
                        <span class="size">${size}</span>
                        <span class="type">${type}</span>
                    </div>
                    <button class="remove-btn" data-index="${i}">✕</button>
                </div>
            `;
        }

        this.fileListContainer.innerHTML = html;

        this.fileListContainer.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.removeFile(parseInt(e.target.dataset.index));
            });
        });
    }

    escape(text) {
        const d = document.createElement('div');
        d.textContent = text;
        return d.innerHTML;
    }

    // ─── CONVERSÃO ────────────────────────────────────────────────

    async convertFiles() {
        if (this.files.length === 0) return;

        this.convertBtn.disabled = true;
        this.convertBtn.textContent = '⏳ convertendo...';
        this.resultsSection.hidden = true;
        this.resultsContainer.innerHTML = '';

        const format = this.formatSelect.value;
        const quality = parseInt(this.qualityRange.value) / 100;
        const results = [];

        for (const file of this.files) {
            try {
                const result = await this.convert(file, format, quality);
                results.push(result);
            } catch (err) {
                results.push({ name: file.name, success: false, error: err.message });
            }
        }

        this.showResults(results);
        this.convertBtn.textContent = '⚡ converter';
        this.convertBtn.disabled = false;
    }

    async convert(file, format, quality) {
        if (file.type.startsWith('image/')) {
            return this.convertImage(file, format, quality);
        }
        if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
            return this.convertText(file, format);
        }
        return { name: file.name, success: false, error: 'formato não suportado' };
    }

    convertImage(file, format, quality) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);

                    const mime = `image/${format === 'jpg' ? 'jpeg' : format}`;
                    const dataUrl = canvas.toDataURL(mime, quality);
                    const baseName = file.name.replace(/\.[^.]+$/, '');
                    const outName = `${baseName}.${format}`;

                    resolve({
                        name: outName,
                        success: true,
                        dataUrl: dataUrl,
                        format: format,
                        isImage: true
                    });
                };
                img.onerror = () => reject(new Error('erro ao carregar imagem'));
                img.src = e.target.result;
            };
            reader.onerror = () => reject(new Error('erro ao ler arquivo'));
            reader.readAsDataURL(file);
        });
    }

    convertText(file, format) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                let text = e.target.result;
                const baseName = file.name.replace(/\.[^.]+$/, '');
                const outName = `${baseName}.${format}`;

                if (format === 'md') {
                    text = `# ${baseName}\n\n${text}`;
                }

                const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
                const dataUrl = URL.createObjectURL(blob);

                resolve({
                    name: outName,
                    success: true,
                    dataUrl: dataUrl,
                    format: format,
                    isImage: false
                });
            };
            reader.onerror = () => reject(new Error('erro ao ler arquivo'));
            reader.readAsText(file);
        });
    }

    showResults(results) {
        this.resultsSection.hidden = false;
        let html = '';
        let ok = 0;

        for (const r of results) {
            if (r.success) {
                ok++;
                html += `
                    <div class="result-item">
                        ${r.isImage ? `<img src="${r.dataUrl}" alt="${r.name}" class="preview">` : ''}
                        <strong>${this.escape(r.name)}</strong>
                        <a href="${r.dataUrl}" download="${r.name}" class="btn btn-primary">📥 baixar</a>
                    </div>
                `;
            } else {
                html += `
                    <div class="result-item" style="border-color:#e06b7a;">
                        <strong>❌ ${this.escape(r.name)}</strong>
                        <p style="color:#e06b7a;font-size:0.8rem;">${this.escape(r.error)}</p>
                    </div>
                `;
            }
        }

        this.resultTitle.textContent = `✅ ${ok} de ${results.length} arquivo(s) convertido(s)`;
        this.resultsContainer.innerHTML = html;
    }
}

document.addEventListener('DOMContentLoaded', () => new FileForgeWeb());