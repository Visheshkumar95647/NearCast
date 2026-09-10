from pydantic import BaseModel, EmailStr


class UserProfileUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserProfileResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool