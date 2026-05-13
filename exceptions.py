from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

# ── 1. Handle Pydantic validation errors (422) ────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field":   " → ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type":    error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={"errors": errors, "message": "Validation failed"}
    )

# ── 2. Handle DB errors (500) ─────────────────────────
@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"message": "Database error occurred"}
        # don't expose the real error — security risk!
    )

# ── 3. Catch ALL unhandled exceptions ─────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )