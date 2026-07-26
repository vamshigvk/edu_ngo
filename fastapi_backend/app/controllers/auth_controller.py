"""Authentication endpoints: register, login (OAuth2), current user."""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import RegisterRequest, Token
from app.schemas.user import UserRead
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await auth_service.register(db, payload)


@router.post("/login", response_model=Token, summary="Obtain a JWT access token")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # OAuth2 password flow: the `username` field carries the user's email.
    user = await auth_service.authenticate(db, form.username, form.password)
    return Token(access_token=auth_service.issue_token(user))


@router.get("/me", response_model=UserRead, summary="Get the current authenticated user")
async def me(current_user: User = Depends(get_current_user)):
    return current_user
