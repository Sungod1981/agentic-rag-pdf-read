# Web Server (FastAPI)

Location: `app/web/server.py`

Purpose
- Provides a small web UI and JSON API for uploading PDFs and chatting with
  the agent scoped to a single uploaded document. The server mounts static
  assets and templates from `app/web/static` and `app/web/templates`.

Endpoints
- `GET /` — returns the main HTML page where users can upload a PDF and ask
  questions.
- `POST /api/ingest` — accepts a PDF upload (`multipart/form-data`), ingests
  the file into a fresh in-memory FAISS store, and sets the active agent to be
  used for subsequent `/api/chat` calls.
- `POST /api/chat` — accept a JSON payload `{"question": "..."}` and return
  `{"answer": "..."}`. Requires a prior `/api/ingest` call to set the active
  document; otherwise it returns a JSON error.

Notes
- The server uses a single `current_agent` representing the most-recently
  uploaded document. This is a simple design choice for demo purposes; you can
  extend the server to persist per-upload indices and manage multiple documents.
- Ensure `python-multipart` is installed to accept file uploads.
