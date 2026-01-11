from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    print(f"DEBUG: Checking for user with email: '{user_in.email}'")
    user = get_user_by_email(db, email=user_in.email)
    print(f"DEBUG: Found user: {user}")
    
    if user:
        print("DEBUG: Raising 400 - User exists")
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    try:
        user = create_user(db, user_in)
        return user
    except Exception as e:
        # Log the error (print it for now so it shows in console)
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@router.post("/token", response_model=Token)
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
