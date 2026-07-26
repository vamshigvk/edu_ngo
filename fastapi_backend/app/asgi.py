"""ASGI entrypoint.

Run with:  uvicorn app.asgi:application --reload
"""
from app.main import create_app

application = create_app()
