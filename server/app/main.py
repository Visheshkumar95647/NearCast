from fastapi import FastAPI

app = FastAPI(
    title="Nearby API",
    description="Privacy-first hyperlocal social discovery platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "nearby-api"
    }