import logging
import time

from fastapi import FastAPI, Request

from app.access import router as access_router
from app.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Space Access Control API",
    description="API locale de contrôle d'accès du vaisseau",
    version="1.0.0"
)

app.include_router(access_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)

    logger.info(
        "HTTP request completed",
        extra={
            "event": "http_request",
            "details": {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        },
    )
    return response


@app.get("/")
def health_check():
    return {
        "status": "online",
        "message": "Space Access Control API fonctionne"
    }
