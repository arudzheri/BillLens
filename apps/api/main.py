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
            .links { margin-top: 16px; font-size: 0.875rem; }
            .links a { color: #2563eb; text-decoration: none; margin-right: 12px; }
            pre { background: #0f172a; color: #f8fafc; padding: 16px; border-radius: 8px; overflow-x: auto; margin-top: 24px; max-height: 400px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>BillLens Search</h1>
            <p>Ask natural-language questions to analyze UK legislation, parliamentary debates, and votes.</p>
            <div class="search-box">
                <input type="text" id="userQuery" placeholder="Ask a question..." value="Who is the prime minister of the UK?">
                <button onclick="askQuestion()">Search</button>
            </div>
            <div class="links">
                <a href="/docs" target="_blank">Interactive Swagger Docs</a>
                <a href="/redoc" target="_blank">ReDoc</a>
                <a href="/health" target="_blank">Health Check</a>
            </div>
            <pre id="output">Results will appear here...</pre>
        </div>

        <script>
            async function askQuestion() {
                const queryText = document.getElementById('userQuery').value;
                const outputEl = document.getElementById('output');
                outputEl.innerText = 'Searching parliamentary records...';

                try {
                    const response = await fetch('/api/v1/questions', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question: queryText })
                    });
                    const data = await response.json();
                    outputEl.innerText = JSON.stringify(data, null, 2);
                } catch (err) {
                    outputEl.innerText = 'Error processing query: ' + err.message;
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