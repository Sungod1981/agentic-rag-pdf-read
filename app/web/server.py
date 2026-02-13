from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging

from ..main import build_components
from ..ingestion.pdf_loader import PdfLoader
from ..retrieval.faiss_store import FaissVectorStore
from ..retrieval.retriever import SemanticRetriever
import shutil
import os
import pathlib
import markdown

logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chat UI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="app/web/templates")
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# Build shared components once on startup (embedder + settings + default LLM)
# Note: we will create a per-upload FAISS store so each uploaded PDF can be
# queried in isolation. `current_agent` will point to the agent for the
# most-recently uploaded document.
settings, embedder, _, _, llm, _ = build_components()

# Prepare uploads folder
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Current active store/agent created when a PDF is uploaded
current_store = None
current_agent = None




@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def _build_docs_tree(root: str):
    """Return a nested dict/list of files and folders under `root` (docs/).

    The structure is a list of entries: {'name': str, 'path': str, 'is_dir': bool, 'children': [...]}
    """
    root_path = pathlib.Path(root)
    tree = []
    if not root_path.exists():
        return tree

    for p in sorted(root_path.iterdir()):
        entry = {"name": p.name, "path": str(p.relative_to(root_path)), "is_dir": p.is_dir()}
        if p.is_dir():
            # children
            entry["children"] = _build_docs_tree(str(p))
        tree.append(entry)
    return tree


@app.get("/docs", response_class=HTMLResponse)
def docs_index(request: Request):
    """Render a simple docs tree and link to README files."""
    docs_root = os.path.join(os.getcwd(), "docs")
    tree = _build_docs_tree(docs_root)
    # If top-level README exists, link to it
    readme = None
    readme_path = os.path.join(docs_root, "README_DOCS.md")
    if os.path.exists(readme_path):
        readme = "README_DOCS.md"
    return templates.TemplateResponse("docs_index.html", {"request": request, "tree": tree, "readme": readme})


@app.get("/docs/view", response_class=HTMLResponse)
def docs_view(request: Request, file: str):
    """Render a specific markdown file from the `docs/` directory as HTML."""
    # prevent path traversal
    docs_root = pathlib.Path(os.path.join(os.getcwd(), "docs")).resolve()
    target = (docs_root / file).resolve()
    if not str(target).startswith(str(docs_root)) or not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found or invalid path")

    text = target.read_text(encoding="utf-8")
    html = markdown.markdown(text, extensions=["fenced_code", "tables", "toc"])
    return templates.TemplateResponse("docs_view.html", {"request": request, "content": html, "file": file})


@app.post("/api/chat")
async def chat_endpoint(req: Request):
    try:
        payload = await req.json()
        q = payload.get("question", "").strip()
        if not q:
            return JSONResponse({"error": "question required"}, status_code=400)

        # Use the current agent bound to the uploaded PDF, if present.
        global current_agent
        if current_agent is None:
            return JSONResponse({"error": "no document uploaded; please upload a PDF first"}, status_code=400)

        resp = current_agent.answer(q)
        return JSONResponse({"answer": resp})
    except Exception as exc:
        logger.exception("Error in chat endpoint")
        return JSONResponse({"error": str(exc)}, status_code=500)



@app.post("/api/ingest")
async def ingest_endpoint(file: UploadFile = File(...)):
    """Accept a PDF upload, ingest it into a FAISS store, and set the
    active agent to serve chat queries only on this document.
    """
    # Validate content type loosely
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse({"error": "only PDF files are supported"}, status_code=400)

    try:
        dest_path = os.path.join(UPLOAD_DIR, file.filename)
        # Save uploaded file to disk
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Ingest: load, chunk, embed, create a dedicated FAISS store
        loader = PdfLoader()
        docs = loader.load(dest_path)
        texts = [d.text for d in docs]
        embeddings = embedder.embed(texts)

        if not embeddings:
            return JSONResponse({"error": "no text extracted from PDF"}, status_code=400)

        # Create a fresh in-memory FAISS store for this upload
        dim = len(embeddings[0])
        store = FaissVectorStore(dim)
        store.add(docs, embeddings)

        # Create a retriever and agent bound to this store
        retriever = SemanticRetriever(embedder, store)
        from ..agent.agent import RagAgent

        agent = RagAgent(retriever, llm, top_k=settings.top_k, similarity_threshold=settings.similarity_threshold)

        # Set as current active agent
        global current_store, current_agent
        current_store = store
        current_agent = agent

        return JSONResponse({"status": "ok", "filename": file.filename})
    except Exception as exc:
        logger.exception("Error ingesting uploaded PDF")
        return JSONResponse({"error": str(exc)}, status_code=500)
