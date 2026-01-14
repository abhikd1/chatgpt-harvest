function captureHTML() {
    const selection = window.getSelection();
    if (selection.rangeCount > 0 && selection.toString().trim().length > 0) {

        // 1. Get the raw selected elements
        const range = selection.getRangeAt(0);
        const container = document.createElement('div');
        container.appendChild(range.cloneContents());

        // 2. THIS IS THE MAGIC FIX 🪄
        // We assume the classes (like 'hljs-keyword', 'text-blue-500') 
        // are doing the heavy lifting for colors.
        // ChatGPT uses Tailwind + HLJS classes. 
        // We need to make sure we keep the 'class' attributes.
        // The cloneContents() DOES keep classes, but we need the CSS.

        return container.innerHTML;
    }

    // ... fallback code ...
    const selectors = [
        'article.w-full:last-of-type',
        '[data-message-author-role="assistant"]:last-of-type',
        '.markdown.prose',
        '.model-response-text:last-of-type',
        '[data-test-id="model-response"]:last-of-type',
        '[data-test-render-count]:last-of-type',
        'article:last-of-type'
    ];

    for (const selector of selectors) {
        const elem = document.querySelector(selector);
        if (elem && elem.innerHTML.trim().length > 10) {
            return elem.innerHTML;
        }
    }
    return '';
}
