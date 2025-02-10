from fastapi import FastAPI

from app.api.v1 import github
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(github.router, prefix="/github", tags=["github"])
