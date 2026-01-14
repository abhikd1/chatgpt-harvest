// OPTIMIZED BOOKMARKLET - Fast, Clean, UI-Faithful Capture
// Strips heavy DOM elements (Monaco editors, SVGs) for instant rendering

javascript: (function () {
    let html = '';
    let source = window.location.hostname;

    // Try to get selected content first
    let selection = window.getSelection();
    if (selection.rangeCount > 0 && selection.toString().trim()) {
        let range = selection.getRangeAt(0);
        let container = document.createElement('div');
        container.appendChild(range.cloneContents());
        html = cleanHTML(container);
        source = 'Selected Content';
    }

    // If no selection, try to find the last AI response
    if (!html) {
        // ChatGPT - Updated selectors for 2026 UI
        let selectors = [
            'article[data-testid^="conversation-turn"]:last-of-type',
            'div[data-message-author-role="assistant"]:last-of-type',
            'article.w-full:last-of-type',
            '.markdown.prose:last-of-type',
            '.agent-turn:last-of-type',
            '.text-message:last-of-type'
        ];

        for (let selector of selectors) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = cleanHTML(elem);
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
            '.response-container:last-of-type',
            'model-response:last-of-type'
        ];

        for (let selector of geminiSelectors) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = cleanHTML(elem);
                source = 'Gemini';
                break;
            }
        }
    }

    // Claude
    if (!html) {
        let claudeSelectors = [
            '[data-test-render-count]:last-of-type',
            '.font-claude-message:last-of-type',
            'div[class*="font-claude"]:last-of-type'
        ];

        for (let selector of claudeSelectors) {
            let elem = document.querySelector(selector);
            if (elem) {
                html = cleanHTML(elem);
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
                html = cleanHTML(elem);
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

    // CLEAN HTML - Remove heavy elements that block rendering
    function cleanHTML(elem) {
        let clone = elem.cloneNode(true);

        // Remove Monaco editors (massive DOM bloat)
        clone.querySelectorAll('.monaco-editor, [class*="monaco-"]').forEach(el => {
            // Keep the text content, remove the editor UI
            let code = el.textContent || el.innerText;
            if (code.trim()) {
                let pre = document.createElement('pre');
                let codeEl = document.createElement('code');
                codeEl.textContent = code;
                pre.appendChild(codeEl);
                el.replaceWith(pre);
            } else {
                el.remove();
            }
        });

        // Remove SVG icons (not needed in saved version)
        clone.querySelectorAll('svg[width="1em"]').forEach(el => el.remove());

        // Remove action buttons (copy, download, etc.)
        clone.querySelectorAll('[class*="action"], [class*="button"], button').forEach(el => {
            if (!el.textContent.trim()) el.remove();
        });

        // Remove empty divs that are just layout containers
        clone.querySelectorAll('div:empty').forEach(el => el.remove());

        return clone.innerHTML;
    }
})();
