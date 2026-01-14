document.getElementById('captureBtn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = '⏳ Capturing...';
    statusDiv.className = 'status';
    statusDiv.style.display = 'block';

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: captureHTML
        });

        const html = results[0].result;

        if (!html || html.length < 10) {
            statusDiv.className = 'status error';
            statusDiv.textContent = '❌ No content found!';
            return;
        }

        const response = await fetch('http://localhost:8766', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                html: html,
                source: tab.url
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            statusDiv.className = 'status success';
            // Show the URL explicitly for debugging
            statusDiv.innerHTML = `
                ✅ SAVED!<br>
                <div style="font-size:0.8em; margin:5px 0; color:#ddd; word-break:break-all;">
                    ${data.url || 'No URL received!'}
                </div>
                <a href="${data.url}" target="_blank" style="color:#00ff00; text-decoration:underline; font-weight:bold; display:block; margin-top:5px; border:1px solid #00ff00; padding:5px; border-radius:4px;">
                    🌍 CLICK TO VIEW
                </a>
            `;
        } else {
            throw new Error(data.message);
        }

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '❌ Server not running! Run: python capture_server.py';
    }
});

function captureHTML() {
    let html = '';
    let source = 'Unknown';

    /* 1️⃣ PRIORITY: USER SELECTION */
    let sel = window.getSelection();
    if (sel && sel.rangeCount > 0 && sel.toString().trim().length > 0) {
        let r = sel.getRangeAt(0);
        let d = document.createElement('div');
        d.appendChild(r.cloneContents());
        html = d.innerHTML;
        source = 'Selection';
    }

    /* 2️⃣ ChatGPT (Automatic Capture All) */
    if (!html) {
        let blocks = document.querySelectorAll('article div[data-message-author-role="assistant"]');
        if (blocks.length) {
            html = Array.from(blocks).map(b => b.innerHTML).join('<hr style="border:1px solid #eee; margin:2em 0;">');
            source = 'ChatGPT (All)';
        }
    }

    /* 3️⃣ Claude */
    if (!html) {
        let c = document.querySelectorAll('[data-test-render-count]');
        if (c.length) {
            html = Array.from(c).map(e => e.innerHTML).join('<hr style="border:1px solid #eee; margin:2em 0;">');
            source = 'Claude (All)';
        }
    }

    if (!html) return '';

    // ✨ 100% CHATGPT NATIVE CSS (Provided by User)
    const styleFix = `
        <style>
            :root { 
                --spacing: .25rem; 
                --text-sm: .875rem; 
                --text-sm--line-height: calc(1.25/.875); 
                --text-base: 1rem; 
                --text-base--line-height: calc(1.5/1); 
                --radius-2xl: 1rem; 
                --default-font-family: "ui-sans-serif","-apple-system","system-ui","Segoe UI","Helvetica","Apple Color Emoji","Arial","sans-serif","Segoe UI Emoji","Segoe UI Symbol"; 
                --default-mono-font-family: "ui-monospace","SFMono-Regular","SF Mono","Menlo","Consolas","Liberation Mono","monospace"; 
                --mkt-header-height: calc(16*var(--spacing));
                --default-theme-user-msg-bg: #e9e9e980; 
                --default-theme-user-msg-text: #0d0d0d; 
                --default-theme-submit-btn-bg: #000; 
                --default-theme-submit-btn-text: #fff; 
                --default-theme-secondary-btn-bg: #ececec; 
                --default-theme-secondary-btn-text: #0d0d0d; 
                --default-theme-user-selection-bg: #339cff59; 
                --default-theme-attribution-highlight-bg: #ffeeb8; 
                --default-theme-entity-accent: #0169cc; 
                --sidebar-rail-width: calc(13*var(--spacing)); 
                --header-height: calc(13*var(--spacing));
                --white: #fff; 
                --black: #000; 
                --gray-50: #f9f9f9; 
                --gray-100: #ececec; 
                --gray-200: #e3e3e3; 
                --gray-800: #212121; 
                --gray-950: #0d0d0d; 
                --red-500: #e02e2a; 
            }

            body.captured-content {  
                background-color: var(--bg-primary, #fff);
                color: var(--text-primary, #0d0d0d);
                font-family: var(--default-font-family);
                font-size: .875em;
                line-height: 1.71429;
                /* CSS Variables provided by user */
                --tw-contain-size:  inline-size;  
                --message-surface:  #e9e9e980;  
                --composer-surface:  var(--message-surface);  
                --composer-surface-primary:  var(--main-surface-primary);  
                --dot-color:  var(--black);  
                --text-primary:  var(--gray-950);  
                --text-primary-inverse:  var(--gray-100);  
                --text-secondary:  #0009;  
                --text-danger:  var(--red-500);  
                --border-light:  #0000001a;  
                --border-xheavy:  #00000040;  
                --border-sharp:  #0000000d;  
                --main-surface-primary:  var(--white);  
                --main-surface-primary-inverse:  var(--gray-800);  
                --main-surface-secondary:  var(--gray-50);  
                --main-surface-tertiary:  var(--gray-100);  
                --sidebar-surface-primary:  var(--gray-50);  
                --sidebar-surface-secondary:  var(--gray-100);  
                --sidebar-surface-tertiary:  var(--gray-200);  
                --scrollbar-color:  #0000001a;  
                --scrollbar-color-hover:  #0003; 
                --tw-prose-body:  var(--text-primary);  
                --tw-prose-headings:  var(--text-primary);  
                --tw-prose-lead:  var(--text-primary);  
                --tw-prose-links:  var(--text-primary);  
                --tw-prose-bold:  var(--text-primary);  
                --tw-prose-counters:  var(--text-primary);  
                --tw-prose-bullets:  var(--text-primary);  
                --tw-prose-hr:  var(--border-xheavy);  
                --tw-prose-quotes:  var(--text-primary);  
                --tw-prose-captions:  var(--text-secondary);  
                --tw-prose-code:  var(--text-primary);  
                --bg-primary:  #fff;  
                --border-light:  #0d0d0d0d;  
                --text-primary:  #0d0d0d;  
                --text-secondary:  #5d5d5d;  
                --thread-content-max-width:  48rem; 
                --thread-content-margin:  calc(var(--spacing)*16); 
            }

            .content {
                max-width: var(--thread-content-max-width);
                margin: 0 auto;
                padding: var(--thread-content-margin);
            }

            pre { 
                font-family: var(--default-mono-font-family,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace); 
                font-size: .875em; 
                font-weight: 400; 
                line-height: 1.71429; 
                overflow-x: auto;
                background-color: #f7f7f8 !important;
                border-radius: .375rem;
                padding: 1rem !important;
                margin: 1rem 0;
                color: #383a42;
            } 

            code { 
                font-family: var(--default-mono-font-family)!important; 
                font-size: 1em;
            } 

            .prose :where(code):not(:where([class ~ ="not-prose"] *)) { 
                color: var(--tw-prose-code); 
                background-color: var(--gray-100); 
                border-radius: .25rem; 
                padding: .15rem .3rem; 
                font-size: .875em; 
                font-weight: 500;
            }

            .hljs-built_in { color: #c18401; } 
            .hljs-keyword { color: #a626a4; }
            .hljs-string { color: #50a14f; }
            .hljs-comment { color: #a0a1a7; font-style: italic; }
            
            table { border-collapse: collapse; width: 100%; margin: 1em 0; border: 1px solid var(--gray-200); }
            th, td { border: 1px solid var(--gray-200); padding: 8px; }
            th { background-color: var(--gray-50); text-align: left; }
        </style>
    `;

    return styleFix + '<div class="captured-content"><div class="content">' + html + '</div></div>';
}
