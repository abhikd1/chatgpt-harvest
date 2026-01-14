// UPDATED BOOKMARKLET - Works with current ChatGPT/Gemini/Claude interfaces
// This version tries multiple selectors to find AI responses

javascript: (function () {
    let html = '';
    let source = window.location.hostname;

    // Try to get selected content first
    let selection = window.getSelection();
    if (selection.rangeCount > 0 && selection.toString().trim()) {
        let range = selection.getRangeAt(0);
        let container = document.createElement('div');
        container.appendChild(range.cloneContents());
        html = container.innerHTML;
        source = 'Selected Content';
    }

    // If no selection, try to find the last AI response
    if (!html) {
        // ChatGPT - try multiple selectors
        let selectors = [
            'article.w-full:last-of-type',
            '.markdown.prose',
            '[data-message-author-role="assistant"]:last-of-type',
            '.agent-turn:last-of-type',
            '.text-message:last-of-type'
        ];

        for (let selector of selectors) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = elem.innerHTML;
                source = 'ChatGPT';
                break;
            }
        }
    }

    // Gemini
    if (!html) {
        let geminiSelectors = [
            '.model-response-text:last-of-type',
            '[data-test-id="model-response"]:last-of-type',
            '.response-container:last-of-type'
        ];

        for (let selector of geminiSelectors) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = elem.innerHTML;
                source = 'Gemini';
                break;
            }
        }
    }

    // Claude
    if (!html) {
        let claudeSelectors = [
            '[data-test-render-count]:last-of-type',
            '.font-claude-message:last-of-type'
        ];

        for (let selector of claudeSelectors) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = elem.innerHTML;
                source = 'Claude';
                break;
            }
        }
    }

    // Fallback: try to get any article or main content
    if (!html) {
        let fallbacks = ['article:last-of-type', 'main', '.main-content'];
        for (let selector of fallbacks) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = elem.innerHTML;
                break;
            }
        }
    }

    if (!html || html.trim().length < 10) {
        alert('❌ No content found!\n\nTry this:\n1. SELECT the AI response (click and drag)\n2. Click this bookmarklet again');
        return;
    }

    // Send to server
    fetch('http://localhost:8766', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            html: html,
            source: source
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('✅ Render captured!\n\n' + data.message + '\n\nSize: ' + Math.round(html.length / 1024) + ' KB');
            } else {
                alert('❌ Capture failed:\n\n' + data.message);
            }
        })
        .catch(error => {
            alert('❌ Server not running!\n\nStart server:\npython capture_server.py');
        });
})();
