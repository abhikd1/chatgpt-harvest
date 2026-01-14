document.getElementById('captureBtn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = '⏳ Capturing...';
    statusDiv.className = 'status';
    statusDiv.style.display = 'block';

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                // ⚡ ULTIMATE FREEZE LOGIC (Surgical & Selection-Aware)

                function freezeNode(source, target) {
                    const style = window.getComputedStyle(source);
                    let css = "";

                    // 📐 Complete Layout & Visual Set
                    const props = [
                        'color', 'background-color', 'font-family', 'font-size', 'font-weight',
                        'padding', 'margin', 'border', 'border-radius', 'display',
                        'flex', 'flex-direction', 'align-items', 'justify-content',
                        'position', 'width', 'max-width', 'box-sizing'
                    ];

                    props.forEach(p => {
                        css += `${p}: ${style.getPropertyValue(p)}; `;
                    });

                    // 🏁 SPACING LOCK (1.75 for prose, original for specific blocks)
                    if (['P', 'LI', 'LABEL'].includes(source.tagName)) {
                        css += "line-height: 1.75 !important; ";
                    } else {
                        css += `line-height: ${style.getPropertyValue('line-height')}; `;
                    }

                    target.setAttribute('style', css);
                }

                const siteName = (() => {
                    const host = window.location.hostname;
                    if (host.includes('chatgpt') || host.includes('openai')) return 'ChatGPT';
                    if (host.includes('gemini.google')) return 'Gemini';
                    if (host.includes('claude')) return 'Claude';
                    if (host.includes('deepseek')) return 'DeepSeek';
                    return host;
                })();

                const sel = window.getSelection();

                // --- CASE 1: SURGICAL SELECTION ---
                if (sel && sel.toString().trim()) {
                    const range = sel.getRangeAt(0);

                    // Identify elements in range to freeze styles
                    const walker = document.createTreeWalker(range.commonAncestorContainer, NodeFilter.SHOW_ELEMENT);
                    const elementsInRange = [];
                    let node;
                    while (node = walker.nextNode()) {
                        if (range.intersectsNode(node)) elementsInRange.push(node);
                    }

                    // Temp-Freeze live elements to capture their state during clone
                    const history = new Map();
                    elementsInRange.forEach(el => {
                        history.set(el, el.getAttribute('style'));
                        freezeNode(el, el);
                    });

                    // Extract the stylized fragment
                    const fragment = range.cloneContents();

                    // Clean up live DOM immediately
                    elementsInRange.forEach(el => {
                        const original = history.get(el);
                        if (original === null) el.removeAttribute('style');
                        else el.setAttribute('style', original);
                    });

                    const container = document.createElement('div');
                    container.appendChild(fragment);
                    // Remove UI buttons from fragment
                    container.querySelectorAll('svg, button, .sr-only').forEach(x => x.remove());

                    return { html: container.innerHTML, source: `${siteName} (Selection)` };
                }

                // --- CASE 2: AUTOMATIC ASSISTANT BLOCK ---
                let liveEl = document.querySelectorAll('article [data-message-author-role="assistant"]');
                liveEl = liveEl[liveEl.length - 1];
                if (!liveEl) {
                    liveEl = document.querySelector('[data-testid="conversation-turn"]:last-child') || document.querySelector('article');
                }

                if (!liveEl) return { html: '', source: 'None' };

                const clone = liveEl.cloneNode(true);
                const liveNodes = [liveEl, ...Array.from(liveEl.querySelectorAll('*'))];
                const cloneNodes = [clone, ...Array.from(clone.querySelectorAll('*'))];

                for (let i = 0; i < liveNodes.length && i < cloneNodes.length; i++) {
                    freezeNode(liveNodes[i], cloneNodes[i]);
                }

                clone.querySelectorAll('svg, button, .sr-only, [aria-hidden="true"]').forEach(x => x.remove());
                return { html: clone.innerHTML, source: `${siteName} (Message)` };
            }
        });

        if (!results || !results[0].result || results[0].result.html === '') {
            statusDiv.textContent = 'No content found!';
            statusDiv.className = 'status error'; // Ensure error class is applied
            return;
        }

        const scriptResult = results[0].result; // Renamed to avoid conflict with 'data' from fetch response

        const response = await fetch('http://localhost:8771', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                html: scriptResult.html,
                source: scriptResult.source
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            statusDiv.className = 'status success';
            statusDiv.innerHTML = `
                ✅ APPENDED TO LOG!<br>
                <a href="${data.url}" target="_blank" style="color:#00ff00; text-decoration:underline; font-weight:bold; display:block; margin-top:5px; border:1px solid #00ff00; padding:5px; border-radius:4px;">
                    📚 VIEW MASTER HARVEST
                </a>
            `;
        } else {
            throw new Error(data.message);
        }

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '❌ Server not running! Run: python append_server.py';
    }
});


