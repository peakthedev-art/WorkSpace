from fastapi import FastAPI

from app.access import router as access_router

app = FastAPI(
    title="Space Access Control API",
    description="API locale de contrôle d'accès du vaisseau",
    version="1.0.0"
)

app.include_router(access_router)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "message": "Space Access Control API fonctionne"
    }
