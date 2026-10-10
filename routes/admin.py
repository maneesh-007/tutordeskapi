from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.admin import Admin
from schemas.admin import AdminLogin, AdminRegister, ChangePassword, UpdateProfile, TokenRefreshRequest
from utility import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    get_current_admin,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/register")
async def register_admin(admin: AdminRegister, db: Session = Depends(get_db)):
    userexistscheck = db.query(Admin).count()

    if userexistscheck > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already registered.",
        )

    hashpwd = hash_password(admin.password)
    new_admin = Admin(name=admin.name, email=admin.email, password=hashpwd)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "Admin registered successfully."}


@router.post("/login")
async def login_admin(admin: AdminLogin, db: Session = Depends(get_db)):
    user = db.query(Admin).filter(Admin.email == admin.email).first()

    if not user or not verify_password(admin.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    """Exchanges a valid refresh token for a new access token and refresh token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(request.refresh_token)
    if payload is None:
        raise credentials_exception

    # Check that it's a refresh token
    if payload.get("type") != "refresh":
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(Admin).filter(Admin.id == int(user_id)).first()
    if not user:
        raise credentials_exception

    # Issue new access token (and new refresh token)
    new_access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

@router.get("/profile")
async def get_admin_profile(
current_admin: Admin = Depends(get_current_admin),
):
    return {
    "id": current_admin.id,
    "name": current_admin.name,
    "email": current_admin.email,
    }



@router.put("/profile")
async def update_profile(
    profile_data: UpdateProfile,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    current_admin.name = profile_data.name

    db.commit()
    db.refresh(current_admin)

    return {
        "message": "Profile updated successfully.",
        "admin": {
            "id": current_admin.id,
            "name": current_admin.name,
            "email": current_admin.email,
        },
    }


@router.put("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    if not verify_password(password_data.current_password, current_admin.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password.",
        )

    current_admin.password = hash_password(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully."}