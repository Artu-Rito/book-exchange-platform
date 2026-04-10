from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

app = FastAPI()

SALT = "book_exchange_salt_2024"

def get_password_hash(password: str) -> str:
    return hashlib.sha256((password + SALT).encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_email: str

# Простая "БД"
USERS = {
    "test@test.com": {
        "email": "test@test.com",
        "full_name": "Test User",
        "hashed_password": get_password_hash("123456")
    }
}

@app.post("/login-simple", response_model=LoginResponse)
def login_simple(form_data: LoginRequest):
    user = USERS.get(form_data.email)
    
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    return {
        "access_token": "test_token_123",
        "user_email": user["email"]
    }
