from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AdminRegister(BaseModel):
    name: str
    email: EmailStr  # Automatically validates email format (e.g., user@domain.com)
    password: str

    model_config = ConfigDict(from_attributes=True)


class AdminLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


# --- New Schemas ---


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(
        ..., min_length=8, description="New password must be at least 8 characters"
    )

    model_config = ConfigDict(from_attributes=True)


class UpdateProfile(BaseModel):
    name: str = Field(..., min_length=1, description="Updated name of the admin")

    model_config = ConfigDict(from_attributes=True)


class TokenRefreshRequest(BaseModel):
    refresh_token: str