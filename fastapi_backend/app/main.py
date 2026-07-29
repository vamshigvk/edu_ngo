"""FastAPI application factory."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.router import (
    api_router,
    auth_router,
    closeout_router,
    dashboard_router,
    document_router,
    public_router,
    review_router,
    workshop_router,
)
from app.core.config import settings
from app.core.dependencies import require_admin
from app.core.exceptions import register_exception_handlers
from app.openapi import custom_openapi


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup / shutdown hooks (DB pools, caches, etc.) can live here.
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # Routers.
    #   auth        → login/register are public; /auth/me guards itself.
    #   public      → intentionally unauthenticated (apply forms, public reads).
    #   api         → EVERY management endpoint requires an authenticated admin.
    #   dashboard   → each endpoint carries its own role guard.
    app.include_router(auth_router)
    app.include_router(public_router, prefix=settings.api_prefix)
    app.include_router(review_router, prefix=settings.api_prefix)
    app.include_router(document_router, prefix=settings.api_prefix)
    app.include_router(workshop_router, prefix=settings.api_prefix)
    app.include_router(closeout_router, prefix=settings.api_prefix)
    app.include_router(
        api_router, prefix=settings.api_prefix, dependencies=[Depends(require_admin)]
    )
    app.include_router(dashboard_router)

    @app.get("/health", tags=["Health"], summary="Liveness probe")
    async def health():
        return {"status": "ok", "service": settings.app_name, "version": __version__}

    app.openapi = custom_openapi(app)
    return app


app = create_app()
