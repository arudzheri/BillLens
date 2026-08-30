"""
BillLens API Application
"""

from __future__ import annotations

import os
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from .routes import questions

# 1. Initialize FastAPI app FIRST
app = FastAPI(
    title="BillLens API",
    description="AI-powered parliamentary intelligence",
    version="0.1.0",
)

# Global exception handler to return structured JSON errors instead of HTML "Internal Server Error"
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "traceback": traceback.format_exc().splitlines()[-5:],
        },
    )

# 2. Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include routers
app.include_router(questions.router)


# 4. Add root route
@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BillLens - Parliamentary Intelligence</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 40px; background: #f8fafc; color: #0f172a; }
            .container { max-width: 750px; margin: 0 auto; background: white; padding: 32px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
            h1 { margin-top: 0; color: #1e293b; font-size: 1.75rem; }
            p { color: #64748b; line-height: 1.5; }
            .search-box { display: flex; gap: 8px; margin: 24px 0; }
            input[type="text"] { flex: 1; padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 1rem; outline: none; }
            input[type="text"]:focus { border-color: #2563eb; }
            button { padding: 12px 24px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; }
            button:hover { background: #1d4ed8; }
            button:disabled { background: #93c5fd; cursor: not-allowed; }
            .links { margin-top: 16px; font-size: 0.875rem; }
            .links a { color: #2563eb; text-decoration: none; margin-right: 12px; }

            #output { margin-top: 24px; }
            .placeholder { color: #94a3b8; font-style: italic; }
            .error-box { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; padding: 14px 16px; border-radius: 8px; font-size: 0.9rem; }

            .result-card { border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px; }
            .summary { font-size: 1rem; line-height: 1.6; color: #1e293b; margin-bottom: 12px; }
            .confidence-row { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; font-size: 0.85rem; color: #475569; }
            .confidence-bar { flex: 1; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
            .confidence-fill { height: 100%; background: #2563eb; }

            .section { margin-top: 16px; }
            .section h3 { margin: 0 0 6px 0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }
            .section ul { margin: 0; padding-left: 20px; }
            .section li { margin-bottom: 4px; line-height: 1.4; }

            .warnings { background: #fffbeb; border: 1px solid #fde68a; color: #92400e; padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; margin-top: 16px; }

            .sources a { color: #2563eb; text-decoration: none; }
            .sources a:hover { text-decoration: underline; }

            details { margin-top: 16px; }
            summary { cursor: pointer; font-size: 0.8rem; color: #64748b; }
            pre { background: #0f172a; color: #f8fafc; padding: 16px; border-radius: 8px; overflow-x: auto; margin-top: 8px; max-height: 400px; font-size: 0.8rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>BillLens Search</h1>
            <p>Ask natural-language questions to analyze UK legislation, parliamentary debates, and votes.</p>
            <div class="search-box">
                <input type="text" id="userQuery" placeholder="Ask a question..." value="Who is the prime minister of the UK?">
                <button id="searchBtn" onclick="askQuestion()">Search</button>
            </div>
            <div class="links">
                <a href="/docs" target="_blank">Interactive Swagger Docs</a>
                <a href="/redoc" target="_blank">ReDoc</a>
                <a href="/health" target="_blank">Health Check</a>
            </div>
            <div id="output"><p class="placeholder">Results will appear here...</p></div>
        </div>

        <script>
            const input = document.getElementById('userQuery');
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') askQuestion();
            });

            function escapeHtml(str) {
                const div = document.createElement('div');
                div.innerText = str;
                return div.innerHTML;
            }

            function renderList(title, items) {
                if (!items || items.length === 0) return '';
                const lis = items.map(item => `<li>${escapeHtml(item)}</li>`).join('');
                return `<div class="section"><h3>${title}</h3><ul>${lis}</ul></div>`;
            }

            function renderResult(data) {
                const confidencePct = Math.round((data.confidence || 0) * 100);

                let html = '<div class="result-card">';
                html += `<div class="summary">${escapeHtml(data.summary || 'No summary available.')}</div>`;
                html += `
                    <div class="confidence-row">
                        <span>Confidence: ${confidencePct}%</span>
                        <div class="confidence-bar"><div class="confidence-fill" style="width:${confidencePct}%"></div></div>
                    </div>
                `;

                html += renderList('What happened', data.what_happened);
                html += renderList('Legislation', data.legislation);
                html += renderList('Parliamentary activity', data.parliamentary_activity);
                html += renderList('Votes', data.votes);
                html += renderList('Not verified', data.what_did_not_happen);

                if (data.sources && data.sources.length > 0) {
                    const sourceLinks = data.sources.map(s => {
                        const label = escapeHtml(s.title || s.source_type || 'Source');
                        return s.url
                            ? `<li><a href="${s.url}" target="_blank" rel="noopener">${label}</a></li>`
                            : `<li>${label}</li>`;
                    }).join('');
                    html += `<div class="section sources"><h3>Sources</h3><ul>${sourceLinks}</ul></div>`;
                }

                if (data.warnings && data.warnings.length > 0) {
                    html += `<div class="warnings">${data.warnings.map(escapeHtml).join('<br>')}</div>`;
                }

                html += `
                    <details>
                        <summary>View raw JSON</summary>
                        <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
                    </details>
                `;
                html += '</div>';
                return html;
            }

            function extractErrorMessage(errorBody) {
                if (!errorBody) return 'Something went wrong.';
                const detail = errorBody.detail ?? errorBody.message ?? errorBody;
                if (typeof detail === 'string') return detail;
                if (Array.isArray(detail)) {
                    return detail.map(d => d.msg || JSON.stringify(d)).join('; ');
                }
                return JSON.stringify(detail);
            }

            async function askQuestion() {
                const queryText = input.value.trim();
                const outputEl = document.getElementById('output');
                const btn = document.getElementById('searchBtn');

                if (!queryText) {
                    outputEl.innerHTML = '<div class="error-box">Please enter a question before searching.</div>';
                    return;
                }

                btn.disabled = true;
                outputEl.innerHTML = '<p class="placeholder">Searching parliamentary records...</p>';

                try {
                    const response = await fetch('/api/v1/questions', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question: queryText })
                    });

                    let data;
                    try {
                        data = await response.json();
                    } catch (parseErr) {
                        throw new Error('The server returned an unreadable response.');
                    }

                    if (!response.ok) {
                        outputEl.innerHTML = `<div class="error-box">${escapeHtml(extractErrorMessage(data))}</div>`;
                        return;
                    }

                    outputEl.innerHTML = renderResult(data);
                } catch (err) {
                    outputEl.innerHTML = `<div class="error-box">Could not reach BillLens: ${escapeHtml(err.message)}</div>`;
                } finally {
                    btn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "billlens"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready", "service": "billlens"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)