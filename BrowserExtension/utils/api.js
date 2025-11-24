// API communication module
const API_URL = 'http://localhost:8000/predict';

//Send URL to backend API for prediction
export async function send_to_api(url) {
    // Get settings from storage
    const settings = await chrome.storage.local.get([
        'enableML',
        'enableGemini',
        'geminiApiKey'
    ]);

    console.log('[API] Current settings:', {
        enableML: settings.enableML !== false,
        enableGemini: settings.enableGemini === true,
        hasGeminiKey: !!settings.geminiApiKey
    });

    // Determine which method to use
    const useGemini = settings.enableGemini === true && settings.geminiApiKey;

    // Build query parameters
    const params = new URLSearchParams();

    if (useGemini) {
        // Use Gemini API (takes priority if enabled)
        params.set('use_gemini', 'true');
    }
    // If only ML or both disabled, no params needed (default to ML behavior)

    const apiUrl = params.toString() ? `${API_URL}?${params}` : API_URL;

    // Build headers
    const headers = {
        'Content-Type': 'application/json',
    };

    // Add Gemini API key if using Gemini
    if (useGemini && settings.geminiApiKey) {
        headers['X-Gemini-API-Key'] = settings.geminiApiKey;
    }

    console.log('[API] Sending request to:', apiUrl);
    console.log('[API] Method:', useGemini ? 'Gemini only' : 'ML only');

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                'check_url': url,
                'timestamp': Date.now()
            }),
        });

        if (!response.ok) {
            const message = await response.text();
            throw new Error(`API request failed: ${response.status} ${message}`);
        }

        const data = await response.json();
        console.log('[API] Response:', data);

        return data;
    } catch (error) {
        console.error('[API] Request failed:', error);
        throw error;
    }
}

