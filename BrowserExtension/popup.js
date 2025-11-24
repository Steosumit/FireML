// Popup script for FireML settings
console.log('[FireML Popup] Initializing...');

// DOM elements
const enableMLCheckbox = document.getElementById('enableML');
const enableGeminiCheckbox = document.getElementById('enableGemini');
const geminiConfig = document.getElementById('geminiConfig');
const geminiApiKeyInput = document.getElementById('geminiApiKey');
const saveGeminiKeyBtn = document.getElementById('saveGeminiKey');
const statusMessage = document.getElementById('statusMessage');
const mlStatus = document.getElementById('mlStatus');
const geminiStatus = document.getElementById('geminiStatus');

// Load saved settings
chrome.storage.local.get(['enableML', 'enableGemini', 'geminiApiKey'], (result) => {
    console.log('[FireML Popup] Loaded settings:', result);

    enableMLCheckbox.checked = result.enableML !== false; // default true
    enableGeminiCheckbox.checked = result.enableGemini === true; // default false

    if (result.geminiApiKey) {
        geminiApiKeyInput.value = result.geminiApiKey;
    }

    updateUI();
    updateStatus();
});

// Toggle ML Model
enableMLCheckbox.addEventListener('change', () => {
    const enabled = enableMLCheckbox.checked;
    chrome.storage.local.set({ enableML: enabled }, () => {
        console.log('[FireML Popup] ML Model:', enabled ? 'enabled' : 'disabled');
        updateStatus();
    });
});

// Toggle Gemini API
enableGeminiCheckbox.addEventListener('change', () => {
    const enabled = enableGeminiCheckbox.checked;
    updateUI();

    chrome.storage.local.set({ enableGemini: enabled }, () => {
        console.log('[FireML Popup] Gemini API:', enabled ? 'enabled' : 'disabled');
        updateStatus();
    });
});

// Save Gemini API Key
saveGeminiKeyBtn.addEventListener('click', () => {
    const apiKey = geminiApiKeyInput.value.trim();

    if (!apiKey) {
        showStatus('Please enter an API key', 'error');
        return;
    }

    // Basic validation (Gemini API keys start with 'AIza')
    if (!apiKey.startsWith('AIza')) {
        showStatus('Invalid API key format. Gemini keys start with "AIza"', 'error');
        return;
    }

    chrome.storage.local.set({ geminiApiKey: apiKey }, () => {
        console.log('[FireML Popup] API key saved');
        showStatus('API key saved successfully!', 'success');
        updateStatus();
    });
});

// Update UI based on toggles
function updateUI() {
    if (enableGeminiCheckbox.checked) {
        geminiConfig.classList.remove('hidden');
    } else {
        geminiConfig.classList.add('hidden');
    }
}

// Update status indicators
function updateStatus() {
    chrome.storage.local.get(['enableML', 'enableGemini', 'geminiApiKey'], (result) => {
        // ML Status
        if (result.enableML !== false) {
            mlStatus.textContent = 'Active';
            mlStatus.style.color = '#16a34a';
        } else {
            mlStatus.textContent = 'Disabled';
            mlStatus.style.color = '#64748b';
        }

        // Gemini Status
        if (result.enableGemini && result.geminiApiKey) {
            geminiStatus.textContent = 'Active';
            geminiStatus.style.color = '#16a34a';
        } else if (result.enableGemini) {
            geminiStatus.textContent = 'Missing API Key';
            geminiStatus.style.color = '#dc2626';
        } else {
            geminiStatus.textContent = 'Disabled';
            geminiStatus.style.color = '#64748b';
        }
    });
}

// Show status message
function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message status-${type}`;
    statusMessage.classList.remove('hidden');

    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, 3000);
}

console.log('[FireML Popup] Initialized successfully');

