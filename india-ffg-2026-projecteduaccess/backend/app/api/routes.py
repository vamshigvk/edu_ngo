from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.session import get_db
from app.models.application import Application
from app.models.notice import Notice
from app.models.user import User
from app.schemas.auth import (
    ApplicationRequest,
    ApprovalRequest,
    NoticeRequest,
    SignInRequest,
    SignUpRequest,
)
from app.services.seed_service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/auth/signup")
def signup(payload: SignUpRequest, db: Session = Depends(get_db)) -> dict:
    role = payload.role.lower()
    if role not in {"admin", "mentor", "mentee", "student"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing = db.query(User).filter(User.email == str(payload.email).lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        password_salt="",
        full_name=payload.full_name,
        role=role,
        status="pending",
        verified_as=None,
        token=None,
        created_at="now",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, role)
    user.token = token
    db.commit()
    db.refresh(user)

    logger.info("User signed up", extra={"email": str(payload.email).lower(), "role": role})
    return {"id": user.id, "email": str(payload.email).lower(), "role": role, "status": "pending", "token": token}


@router.post("/auth/signin")
def signin(payload: SignInRequest, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.email == str(payload.email).lower()).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id, user.role)
    user.token = token
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "status": user.status,
        "verified_as": user.verified_as,
        "token": token,
    }


@router.get("/me")
def me(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        payload = decode_access_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or user.token != token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "status": user.status,
        "verified_as": user.verified_as,
    }


@router.get("/users")
def list_users(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)) -> list[dict]:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        payload = decode_access_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    requester = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not requester or requester.token != token or requester.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    users = db.query(User).order_by(User.id).all()
    return [
        {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role, "status": user.status, "verified_as": user.verified_as}
        for user in users
    ]


@router.put("/users/{user_id}/approve")
def approve_user(user_id: int, payload: ApprovalRequest, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        payload_jwt = decode_access_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    requester = db.query(User).filter(User.id == int(payload_jwt["sub"])).first()
    if not requester or requester.token != token or requester.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "approved"
    user.verified_as = payload.verified_as or "student"
    db.commit()
    return {"ok": True}


@router.get("/notices")
def notices(role: Optional[str] = None, db: Session = Depends(get_db)) -> list[dict]:
    query = db.query(Notice)
    if role:
        query = query.filter(Notice.role == role)
    rows = query.order_by(Notice.id.desc()).all()
    return [{"id": item.id, "title": item.title, "body": item.body, "role": item.role, "created_at": item.created_at} for item in rows]


@router.post("/notices")
def create_notice(payload: NoticeRequest, authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "", 1).strip()
    try:
        payload_jwt = decode_access_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    requester = db.query(User).filter(User.id == int(payload_jwt["sub"])).first()
    if not requester or requester.token != token or requester.role != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    notice = Notice(title=payload.title, body=payload.body, role=payload.role, created_at="now")
    db.add(notice)
    db.commit()
    return {"ok": True}


@router.get("/applications")
def applications(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.query(Application).order_by(Application.id.desc()).all()
    return [{"id": item.id, "applicant_email": item.applicant_email, "applicant_name": item.applicant_name, "program": item.program, "status": item.status, "created_at": item.created_at} for item in rows]


@router.post("/applications")
def create_application(payload: ApplicationRequest, db: Session = Depends(get_db)) -> dict:
    application = Application(applicant_email=str(payload.applicant_email), applicant_name=payload.applicant_name, program=payload.program, status="submitted", created_at="now")
    db.add(application)
    db.commit()
    return {"ok": True}


@router.get("/recommendations")
def recommendations(role: Optional[str] = None) -> list[dict]:
    return []


@router.get("/resources")
def resources() -> list[dict]:
    return []


@router.get("/matches")
def matches() -> list[dict]:
    return []


@router.get("/checkins")
def checkins() -> list[dict]:
    return []
