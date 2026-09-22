from fastapi import FastAPI

app = FastAPI(
    title="Space Access Control API",
    description="API locale de contrôle d'accès du vaisseau",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {
        "Hello wolrd!"
    }