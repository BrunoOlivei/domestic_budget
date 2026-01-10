from app.core.core import get_settings

from app import app

settings = get_settings()


@app.get("/")
def hello_world():
    return {"Hello": "World!", "api_version": settings.api_version}


@app.get("/health")
def health_check():
    return {"status": "ok", "modules": ["finance"]}
