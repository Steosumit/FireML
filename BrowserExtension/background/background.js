// Import API functions
import { send_to_api } from '../utils/api.js';

// Cache functions
const CACHE_KEY = 'fireml:urlCache';
const DEFAULT_TTL_SECONDS = 3600;

const readCache = () => new Promise(resolve => {
    chrome.storage.local.get([CACHE_KEY], result => {
        resolve(result[CACHE_KEY] || {});
    });
});

const writeCache = cache => new Promise(resolve => {
    chrome.storage.local.set({ [CACHE_KEY]: cache }, () => resolve());
});

async function check_cache(url) {
    const cache = await readCache();
    const entry = cache[url];
    if (!entry) {
        return null;
    }

    const now = Date.now();
    if (entry.expiry < now) {
        delete cache[url];
        await writeCache(cache);
        return null;
    }

    return entry.decision;
}

async function store_cache(url, decision, ttl = DEFAULT_TTL_SECONDS) {
    const cache = await readCache();
    cache[url] = {
        decision,
        expiry: Date.now() + ttl * 1000,
    };
    await writeCache(cache);
}

// Intercept URL function - Non-blocking approach
const pendingChecks = new Map();
const ALERT_PAGE_URL = chrome.runtime?.getURL ? chrome.runtime.getURL('ui/index.html') : null;

async function intercept_url(details) {
    const { url = '', tabId, frameId } = details || {};

    // Skip non-http URLs, sub-frames, and our own alert page
    if (!url.startsWith('http') || frameId !== 0 || url.startsWith(ALERT_PAGE_URL)) {
        return;
    }

    // Skip if already checking this tab
    if (pendingChecks.has(tabId)) {
        return;
    }

    const normalizedUrl = url.split('#')[0];

    // Mark as checking
    pendingChecks.set(tabId, normalizedUrl);

    console.log('[FireML] Intercepted URL:', normalizedUrl);

    try {
        // Check cache first
        const cachedDecision = await check_cache(normalizedUrl);
        if (cachedDecision) {
            console.log('[FireML] Cache hit:', cachedDecision);
            await handle_decision(tabId, normalizedUrl, cachedDecision);
            return;
        }

        // Call API
        console.log('[FireML] Calling API for:', normalizedUrl);
        const response = await send_to_api(normalizedUrl);
        const decision = response?.decision || 'safe';

        console.log('[FireML] API decision:', decision);
        await store_cache(normalizedUrl, decision);
        await handle_decision(tabId, normalizedUrl, decision);

    } catch (error) {
        console.error('[FireML] intercept_url failed:', error);
        pendingChecks.delete(tabId);
    }
}

// show_alert(decision, url)
function show_alert(decision, url) {
    if (!ALERT_PAGE_URL) {
        console.warn(`[FireML] - ${decision?.toUpperCase?.() || decision}: ${url}`);
        return;
    }

    const targetUrl = `${ALERT_PAGE_URL}?decision=${encodeURIComponent(decision)}&url=${encodeURIComponent(url)}`;
    chrome.tabs.create({ url: targetUrl });
}

// handle_decision(tabId, url, decision)
async function handle_decision(tabId, url, decision) {
    pendingChecks.delete(tabId);

    const normalizedDecision = (decision || 'safe').toLowerCase();
    const isSuspicious = normalizedDecision === 'suspicious';

    if (isSuspicious) {
        try {
            console.log('[FireML] Blocking suspicious URL:', url);
            // Close the suspicious tab
            await chrome.tabs.remove(tabId);
            // Show alert page
            show_alert(normalizedDecision, url);
        } catch (error) {
            console.error('[FireML] Failed to block suspicious URL:', error);
        }
    } else {
        console.log('[FireML] Allowing safe URL:', url);
    }
}

// Listen to web navigation events - this intercepts ALL new links visited
if (chrome.webNavigation?.onBeforeNavigate) {
    chrome.webNavigation.onBeforeNavigate.addListener(
        details => intercept_url(details),
        { url: [{ schemes: ['http', 'https'] }] }
    );
    console.log('[FireML] Extension loaded - monitoring all HTTP/HTTPS navigation');
} else {
    console.error('[FireML] webNavigation API not available!');
}

