from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=2)
    role: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class ApprovalRequest(BaseModel):
    verified_as: str | None = None


class NoticeRequest(BaseModel):
    title: str = Field(min_length=3)
    body: str = Field(min_length=3)
    role: str


class ApplicationRequest(BaseModel):
    applicant_email: EmailStr
    applicant_name: str = Field(min_length=2)
    program: str = Field(min_length=2)
