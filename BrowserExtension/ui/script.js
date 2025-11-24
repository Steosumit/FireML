
console.log('[FireML UI] Page loaded');

const params = new URLSearchParams(window.location.search);
const decision = (params.get('decision') || 'safe').toLowerCase().trim();
const targetUrl = params.get('url') || 'Unknown URL';

console.log('[FireML UI] Decision:', decision);
console.log('[FireML UI] URL:', targetUrl);

const badge = document.getElementById('badge');
const urlText = document.getElementById('urlText');
const message = document.getElementById('message');

const decisionCopy = {
    safe: {
        label: 'Safe',
        text: 'This URL passed the latest scan.',
        badgeClass: 'badge-safe'
    },
    suspicious: {
        label: 'Suspicious',
        text: 'Blocked because it matches malicious patterns.',
        badgeClass: 'badge-suspicious'
    }
};

const copy = decisionCopy[decision] || decisionCopy.safe;

console.log('[FireML UI] Applying:', copy);

// Update UI elements
badge.innerHTML = copy.label;
badge.className = 'badge ' + copy.badgeClass; // Replace all classes
urlText.innerHTML = targetUrl;
message.innerHTML = copy.text;

console.log('[FireML UI] UI updated successfully');

document.getElementById('closeBtn').addEventListener('click', () => {
    console.log('[FireML UI] Close button clicked');
    if (chrome?.tabs?.getCurrent) {
        chrome.tabs.getCurrent((tab) => {
            if (tab?.id) {
                chrome.tabs.remove(tab.id);
            } else {
                window.close();
            }
        });
    } else {
        window.close();
    }
});
