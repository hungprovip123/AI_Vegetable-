// Vietnamese Vegetable Classification - Frontend JavaScript

class VegetableClassifier {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentFile = null;
    }

    initializeElements() {
        // Main elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.previewArea = document.getElementById('previewArea');
        this.previewImage = document.getElementById('previewImage');
        this.loadingArea = document.getElementById('loadingArea');
        this.resultsArea = document.getElementById('resultsArea');
        this.resultsContent = document.getElementById('resultsContent');

        // Buttons
        this.predictBtn = document.getElementById('predictBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.newPredictionBtn = document.getElementById('newPredictionBtn');
    }

    bindEvents() {
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            console.log('File input change event:', e.target.files);
            if (e.target.files && e.target.files[0]) {
                this.handleFileSelect(e.target.files[0]);
            }
        });

        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadArea.classList.add('dragover');
        });

        this.uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadArea.classList.remove('dragover');
        });

        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        // Button clicks
        this.predictBtn.addEventListener('click', () => {
            this.predictVegetable();
        });

        this.resetBtn.addEventListener('click', () => {
            this.resetUpload();
        });

        this.newPredictionBtn.addEventListener('click', () => {
            this.resetUpload();
        });

        // Click to upload - bind to both upload area and button
        this.uploadArea.addEventListener('click', (e) => {
            // Don't prevent default if clicking on the button
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                return;
            }
            if (!this.uploadArea.classList.contains('d-none')) {
                this.fileInput.click();
            }
        });

        // Bind to the "Chọn Ảnh" button specifically  
        const chooseButton = document.getElementById('chooseFileBtn');
        if (chooseButton) {
            chooseButton.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Choose file button clicked');
                this.fileInput.click();
            });
        }
    }

    handleFileSelect(file) {
        console.log('handleFileSelect called with:', file);
        if (!file) return;

        // Validate file type
        if (!file.type.startsWith('image/')) {
            this.showError('Vui lòng chọn file ảnh (JPG, PNG, WebP)');
            return;
        }

        // Validate file size (10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('File quá lớn. Vui lòng chọn ảnh nhỏ hơn 10MB');
            return;
        }

        this.currentFile = file;
        this.showPreview(file);
    }

    showPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.previewImage.src = e.target.result;
            this.showSection('preview');

            // Add animation
            this.previewArea.classList.add('fade-in-up');
        };
        reader.readAsDataURL(file);
    }

    async predictVegetable() {
        if (!this.currentFile) return;

        this.showSection('loading');

        try {
            const formData = new FormData();
            formData.append('file', this.currentFile);
            formData.append('top_k', 5);

            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError('Có lỗi xảy ra khi nhận diện');
            }

        } catch (error) {
            console.error('Prediction error:', error);
            this.showError(`Lỗi: ${error.message}`);
        }
    }

    showResults(result) {
        const predictions = result.predictions || [];
        const metadata = result.metadata || {};

        let html = `
            <div class="mb-3">
                <div class="d-flex align-items-center mb-2">
                    <img src="${this.previewImage.src}" alt="Analyzed" 
                         style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;" class="me-3">
                    <div>
                        <h6 class="mb-0">${metadata.filename || 'Ảnh đã tải lên'}</h6>
                        <small class="text-muted">Kích thước: ${metadata.image_size ? metadata.image_size.join('x') : 'N/A'}</small>
                    </div>
                </div>
            </div>
        `;

        predictions.forEach((pred, index) => {
            const rank = index + 1;
            const rankClass = rank === 1 ? 'rank-1' : rank === 2 ? 'rank-2' : rank === 3 ? 'rank-3' : 'rank-other';
            const confidenceClass = pred.confidence >= 0.8 ? 'confidence-high' :
                pred.confidence >= 0.5 ? 'confidence-medium' : 'confidence-low';

            html += `
                <div class="result-item d-flex align-items-center">
                    <div class="result-rank ${rankClass} me-3">
                        ${rank}
                    </div>
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <h6 class="mb-0">${this.formatVegetableName(pred.class)}</h6>
                            <span class="badge bg-primary">${pred.percentage}</span>
                        </div>
                        <div class="confidence-bar">
                            <div class="confidence-fill ${confidenceClass}" 
                                 style="width: ${pred.confidence * 100}%"></div>
                        </div>
                    </div>
                </div>
            `;
        });

        // Add top prediction highlight
        if (predictions.length > 0) {
            const topPred = predictions[0];
            const emoji = this.getVegetableEmoji(topPred.class);

            html = `
                <div class="alert alert-success text-center mb-3">
                    <div style="font-size: 3rem; margin-bottom: 10px;">${emoji}</div>
                    <h5 class="mb-1">Đây là: <strong>${this.formatVegetableName(topPred.class)}</strong></h5>
                    <p class="mb-0">Độ chính xác: <strong>${topPred.percentage}</strong></p>
                </div>
            ` + html;
        }

        this.resultsContent.innerHTML = html;
        this.showSection('results');

        // Add animations
        this.resultsArea.classList.add('fade-in-up');

        // Animate confidence bars
        setTimeout(() => {
            document.querySelectorAll('.confidence-fill').forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
        }, 300);
    }

    formatVegetableName(className) {
        // Convert class name to Vietnamese display name
        const nameMapping = {
            'Ca_chua': 'Cà Chua',
            'Ca_rot': 'Cà Rót',
            'Cai_thao': 'Cải Thảo',
            'Cai_be': 'Cải Bẹ',
            'Bau': 'Bầu',
            'Bi_dao': 'Bí Đao',
            'Bi_do': 'Bí Đỏ',
            'Bi_ngoi': 'Bí Ngòi',
            'Bi_xanh': 'Bí Xanh',
            'Bong_bi': 'Bông Bí',
            'Bap_my': 'Bắp Mỹ',
            'Ot_chuong': 'Ớt Chuông',
            'Dua_leo': 'Dưa Leo',
            'Khoai_tay': 'Khoai Tây',
            'Khoai_lang': 'Khoai Lang',
            // Add more mappings as needed
        };

        return nameMapping[className] || className.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    getVegetableEmoji(className) {
        const emojiMapping = {
            'Ca_chua': '🍅',
            'Ca_rot': '🥕',
            'Cai_thao': '🥬',
            'Cai_be': '🥬',
            'Bau': '🥒',
            'Bi_dao': '🎃',
            'Bi_do': '🎃',
            'Bi_ngoi': '🎃',
            'Bi_xanh': '🥒',
            'Bong_bi': '🌼',
            'Bap_my': '🌽',
            'Ot_chuong': '🌶️',
            'Dua_leo': '🥒',
            'Khoai_tay': '🥔',
            'Khoai_lang': '🍠',
        };

        return emojiMapping[className] || '🥬';
    }

    showSection(section) {
        // Hide all sections
        this.uploadArea.classList.add('d-none');
        this.previewArea.classList.add('d-none');
        this.loadingArea.classList.add('d-none');
        this.resultsArea.classList.add('d-none');

        // Show target section
        switch (section) {
            case 'upload':
                this.uploadArea.classList.remove('d-none');
                break;
            case 'preview':
                this.previewArea.classList.remove('d-none');
                break;
            case 'loading':
                this.loadingArea.classList.remove('d-none');
                break;
            case 'results':
                this.resultsArea.classList.remove('d-none');
                break;
        }
    }

    resetUpload() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.showSection('upload');

        // Remove animation classes
        this.previewArea.classList.remove('fade-in-up');
        this.resultsArea.classList.remove('fade-in-up');
    }

    showError(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast position-fixed top-0 end-0 m-3';
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <div class="toast-header bg-danger text-white">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong class="me-auto">Lỗi</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        document.body.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remove toast after hide
        toast.addEventListener('hidden.bs.toast', () => {
            document.body.removeChild(toast);
        });

        // Reset to upload section
        this.showSection('upload');
    }

    // Public API for external use
    async classifyFromUrl(imageUrl) {
        try {
            const response = await fetch('/api/predict-base64', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageUrl,
                    top_k: 5
                })
            });

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('URL classification error:', error);
            throw error;
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.vegetableClassifier = new VegetableClassifier();

    // Add some visual effects
    addScrollEffects();
    addHoverEffects();
});

function addScrollEffects() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addHoverEffects() {
    // Add hover effects to cards
    document.querySelectorAll('.card, .sample-card').forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Utility functions for external use
window.VeggieAPI = {
    classify: (file) => window.vegetableClassifier.classifyFromUrl(file),
    reset: () => window.vegetableClassifier.resetUpload(),
    getSupportedClasses: async () => {
        const response = await fetch('/api/classes');
        return response.json();
    },
    getModelInfo: async () => {
        const response = await fetch('/api/model-info');
        return response.json();
    }
};
