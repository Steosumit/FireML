// send_to_api(url) will be implemented here
const API_URL = 'http://localhost:8000/predict';

export async function send_to_api(url){
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'check_url' : url, 'timestamp': Date.now()}),
    });
    if (!response.ok) {
        const message = await response.text();
        throw new Error(`Inference request failed: ${response.status} ${message}`);
    }
    const data = await response.json();
    return data;
}