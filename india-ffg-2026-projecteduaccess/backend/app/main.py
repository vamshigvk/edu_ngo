from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import ALLOWED_ORIGINS
from app.core.error_handlers import register_exception_handlers
from app.core.logging import get_logger
from app.services.seed_service import seed_database

logger = get_logger(__name__)

app = FastAPI(title="Project EduAccess")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(router)


@app.on_event("startup")
def startup_event():
    seed_database()
    logger.info("Application startup complete")
