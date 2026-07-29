"""Authentication endpoints: register, login (OAuth2), current user, declaration."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.exceptions import ValidationError
from app.models.enums import UserRole
from app.models.profile import MenteeProfile, MentorProfile
from app.models.user import User
from app.schemas.auth import RegisterRequest, Token
from app.schemas.common import MessageResponse
from app.schemas.user import UserRead
from app.schemas.workshop import EnglishSupportRequest
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


@router.post(
    "/declaration",
    response_model=UserRead,
    summary="Sign the mentor/mentee declaration (onboarding)",
)
async def sign_declaration(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Submitting the declaration is what formally activates a mentor/mentee.
    current_user.declaration_signed_at = datetime.now(timezone.utc)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post(
    "/english-support",
    response_model=MessageResponse,
    summary="Opt in/out of the English Language Support Programme",
)
async def english_support(
    payload: EnglishSupportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    model = (
        MentorProfile if current_user.role == UserRole.MENTOR
        else MenteeProfile if current_user.role == UserRole.MENTEE
        else None
    )
    if model is None:
        raise ValidationError("Only mentors and mentees can set this preference.")
    profile = (
        await db.execute(select(model).where(model.user_id == current_user.id))
    ).scalar_one_or_none()
    if profile is None:
        raise ValidationError("No profile found for your account.")
    profile.english_support_opt_in = payload.opt_in
    db.add(profile)
    await db.commit()
    return MessageResponse(message="Preference saved.")
