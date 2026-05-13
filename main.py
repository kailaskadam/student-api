import time, uuid, logging

from fastapi                  import FastAPI, Request
from fastapi.responses        import JSONResponse
from fastapi.exceptions       import RequestValidationError
from fastapi.middleware.cors  import CORSMiddleware
from sqlalchemy.orm           import Session
from typing                   import List

import models, schemas
from database  import engine, get_db, Base
from routers   import students

# ── Logging setup ──────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("api")

# ── Create tables on startup ───────────────────────────
Base.metadata.create_all(bind=engine)

# ── App ────────────────────────────────────────────────
app = FastAPI(
    title="Student Management API",
    version="1.0.0",
    description="FastAPI + PostgreSQL + SQLAlchemy"
)

# ── CORS ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# ── Middleware — logging + timing ──────────────────────
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start      = time.time()

    logger.info(f"[{request_id}] → {request.method} {request.url.path}")

    response = await call_next(request)

    duration = time.time() - start
    logger.info(f"[{request_id}] ← {response.status_code} ({duration:.3f}s)")

    response.headers["X-Request-ID"]   = request_id
    response.headers["X-Process-Time"] = f"{duration:.4f}s"
    return response

# ── Global error handlers ──────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={
        "message": "Validation failed",
        "errors":  exc.errors()
    })

@app.exception_handler(Exception)
async def global_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={
        "message": "Internal server error"
    })

# ── Health check ───────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "Student API running", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

# ── Routes ─────────────────────────────────────────────
app.include_router(students.router, prefix="/students", tags=["Students"])