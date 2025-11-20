// Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// State Management
const state = {
    currentType: 'basic',
    qrData: null
};

// DOM Elements
const elements = {
    typeButtons: document.querySelectorAll('.type-btn'),
    forms: {
        basic: document.getElementById('basic-form'),
        pdf: document.getElementById('pdf-form'),
        api: document.getElementById('api-form'),
        secure: document.getElementById('secure-form')
    },
    inputs: {
        basic: document.getElementById('basic-data'),
        pdfUrl: document.getElementById('pdf-url'),
        pdfFile: document.getElementById('pdf-file'),
        api: document.getElementById('api-endpoint'),
        secure: document.getElementById('secure-url'),
        description: document.getElementById('description')
    },
    pdfOption: document.querySelectorAll('input[name="pdf-option"]'),
    pdfUrlInput: document.getElementById('pdf-url-input'),
    pdfFileInput: document.getElementById('pdf-file-input'),
    qrForm: document.getElementById('qrForm'),
    generateBtn: document.querySelector('.generate-btn'),
    btnText: document.querySelector('.btn-text'),
    loader: document.querySelector('.loader'),
    output: document.getElementById('output'),
    qrImage: document.getElementById('qr-image'),
    resultType: document.getElementById('result-type'),
    resultData: document.getElementById('result-data'),
    resultShortUrl: document.getElementById('result-short-url'),
    resultDescription: document.getElementById('result-description'),
    shortUrlInfo: document.getElementById('short-url-info'),
    descriptionInfo: document.getElementById('description-info'),
    downloadBtn: document.getElementById('download-btn'),
    resetBtn: document.getElementById('reset-btn'),
    errorMessage: document.getElementById('error-message'),
    errorText: document.getElementById('error-text')
};

// Initialize
function init() {
    setupEventListeners();
}

// Event Listeners
function setupEventListeners() {
    // Type button clicks
    elements.typeButtons.forEach(btn => {
        btn.addEventListener('click', handleTypeChange);
    });

    // Form submission
    elements.qrForm.addEventListener('submit', handleFormSubmit);

    // Reset button
    elements.resetBtn.addEventListener('click', resetForm);

    // Download button
    elements.downloadBtn.addEventListener('click', downloadQRCode);
    
    // Method tabs
    document.querySelectorAll('.method-tab').forEach(tab => {
        tab.addEventListener('click', handleMethodTabClick);
    });
    
    // File upload
    const fileInput = elements.inputs.pdfFile;
    const filePlaceholder = document.getElementById('file-placeholder');
    const fileRemoveBtn = document.getElementById('file-remove-btn');
    
    if (filePlaceholder) {
        filePlaceholder.addEventListener('click', () => fileInput.click());
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    if (fileRemoveBtn) {
        fileRemoveBtn.addEventListener('click', handleFileRemove);
    }
}

// Handle method tab click
function handleMethodTabClick(e) {
    const tab = e.currentTarget;
    const method = tab.dataset.method;
    
    // Update active tab
    document.querySelectorAll('.method-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    
    // Show/hide content
    if (method === 'url') {
        elements.pdfUrlInput.classList.remove('hidden');
        elements.pdfFileInput.classList.add('hidden');
        elements.inputs.pdfFile.value = '';
        handleFileRemove();
    } else {
        elements.pdfUrlInput.classList.add('hidden');
        elements.pdfFileInput.classList.remove('hidden');
        elements.inputs.pdfUrl.value = '';
    }
}

// Handle file select
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    // Show file info
    document.getElementById('file-placeholder').classList.add('hidden');
    document.getElementById('file-info').classList.remove('hidden');
    document.getElementById('file-name-display').textContent = file.name;
    document.getElementById('file-size-display').textContent = formatFileSize(file.size);
}

// Handle file remove
function handleFileRemove() {
    elements.inputs.pdfFile.value = '';
    document.getElementById('file-placeholder').classList.remove('hidden');
    document.getElementById('file-info').classList.add('hidden');
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Handle QR type change
function handleTypeChange(e) {
    const button = e.currentTarget;
    const type = button.dataset.type;

    // Update active button
    elements.typeButtons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');

    // Update state
    state.currentType = type;

    // Show/hide appropriate form
    showForm(type);

    // Hide error and output
    hideError();
    hideOutput();
}

// Show appropriate form based on type
function showForm(type) {
    Object.values(elements.forms).forEach(form => form.classList.add('hidden'));
    elements.forms[type].classList.remove('hidden');
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    hideError();

    const formData = getFormData();
    if (!formData) return;

    setLoading(true);

    try {
        const response = await generateQRCode(formData);
        displayQRCode(response);
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

// Get form data based on current type
function getFormData() {
    const description = elements.inputs.description.value.trim();
    let data = {};

    switch (state.currentType) {
        case 'basic':
            const basicData = elements.inputs.basic.value.trim();
            if (!basicData) {
                showError('Please enter a URL or text');
                return null;
            }
            data = { data: basicData };
            break;

        case 'pdf':
            const activeTab = document.querySelector('.method-tab.active');
            const method = activeTab ? activeTab.dataset.method : 'url';
            
            if (method === 'url') {
                const pdfUrl = elements.inputs.pdfUrl.value.trim();
                if (!pdfUrl) {
                    showError('Please enter a PDF URL');
                    return null;
                }
                data = { pdf_url: pdfUrl };
            } else {
                const pdfFile = elements.inputs.pdfFile.files[0];
                if (!pdfFile) {
                    showError('Please select a file to upload');
                    return null;
                }
                // Return FormData for file upload
                const formData = new FormData();
                formData.append('file', pdfFile);
                if (description) {
                    formData.append('description', description);
                }
                return { formData, isFile: true };
            }
            break;

        case 'api':
            const apiEndpoint = elements.inputs.api.value.trim();
            if (!apiEndpoint) {
                showError('Please enter an API endpoint');
                return null;
            }
            data = { api_endpoint: apiEndpoint };
            break;

        case 'secure':
            const secureUrl = elements.inputs.secure.value.trim();
            if (!secureUrl) {
                showError('Please enter a URL to hide');
                return null;
            }
            data = { actual_url: secureUrl };
            break;
    }

    if (description) {
        data.description = description;
    }

    return data;
}

// Generate QR code via API
async function generateQRCode(data) {
    const endpoints = {
        basic: '/basic-qr',
        pdf: '/pdf-qr',
        api: '/api-qr',
        secure: '/secure-qr'
    };

    const endpoint = endpoints[state.currentType];
    const url = `${API_BASE_URL}${endpoint}`;

    let fetchOptions = {
        method: 'POST'
    };

    // Handle file upload (FormData) vs JSON
    if (data.isFile) {
        fetchOptions.body = data.formData;
    } else {
        fetchOptions.headers = {
            'Content-Type': 'application/json'
        };
        fetchOptions.body = JSON.stringify(data);
    }

    const response = await fetch(url, fetchOptions);

    if (!response.ok) {
        let errorMessage = 'Failed to generate QR code';
        try {
            const error = await response.json();
            errorMessage = error.error || errorMessage;
        } catch (e) {
            errorMessage = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
    }

    return await response.json();
}

// Display QR code
function displayQRCode(data) {
    state.qrData = data;

    // Set QR image
    elements.qrImage.src = data.qr_code;

    // Set type
    const typeLabels = {
        basic: 'Basic URL',
        pdf: 'PDF Link',
        api: 'API Endpoint',
        secure: 'Secure URL'
    };
    elements.resultType.textContent = typeLabels[state.currentType];

    // Set data
    const dataValue = data.data || data.pdf_url || data.file_url || data.api_endpoint || data.actual_url;
    elements.resultData.textContent = dataValue;

    // Show short URL if secure type
    if (state.currentType === 'secure' && data.short_url) {
        elements.shortUrlInfo.classList.remove('hidden');
        elements.resultShortUrl.textContent = data.short_url;
    } else {
        elements.shortUrlInfo.classList.add('hidden');
    }

    // Show description if provided
    if (data.description) {
        elements.descriptionInfo.classList.remove('hidden');
        elements.resultDescription.textContent = data.description;
    } else {
        elements.descriptionInfo.classList.add('hidden');
    }

    // Show output section
    showOutput();
}

// Download QR code
function downloadQRCode() {
    if (!state.qrData) return;

    const link = document.createElement('a');
    link.href = state.qrData.qr_code;
    link.download = `qr-code-${state.currentType}-${Date.now()}.png`;
    link.click();
}

// Reset form
function resetForm() {
    elements.qrForm.reset();
    hideOutput();
    hideError();
    state.qrData = null;
}

// UI Helper Functions
function setLoading(isLoading) {
    elements.generateBtn.disabled = isLoading;
    if (isLoading) {
        elements.btnText.classList.add('hidden');
        elements.loader.classList.remove('hidden');
    } else {
        elements.btnText.classList.remove('hidden');
        elements.loader.classList.add('hidden');
    }
}

function showOutput() {
    elements.output.classList.remove('hidden');
    elements.output.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideOutput() {
    elements.output.classList.add('hidden');
}

function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.classList.remove('hidden');
}

function hideError() {
    elements.errorMessage.classList.add('hidden');
}

// Initialize app
init();
