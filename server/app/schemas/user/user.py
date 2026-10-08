from pydantic import BaseModel, EmailStr , UUID4


class UserProfileUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserProfileResponse(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    is_active: bool