from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import os
from dotenv import load_dotenv
from crud import create_criminal, get_criminals, create_case, get_cases, get_cases_by_criminal, delete_criminal, delete_case
from db import get_db_connection, close_db_connection

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Ensure SECRET_KEY and ALGORITHM are loaded
if not SECRET_KEY or not ALGORITHM:
    raise ValueError("Missing SECRET_KEY or ALGORITHM in environment variables")

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 🔐 Helper Functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ Home Route
@app.get("/")
def home():
    return {"message": "Criminal Management System API is Running"}

# ✅ User Registration (MySQL Direct)
@app.post("/register/")
def register_user(username: str, password: str, badge_id: str):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = connection.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = %s OR badge_id = %s", (username, badge_id))
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="User or Badge ID already exists")

    hashed_password = get_password_hash(password)
    
    try:
        cursor.execute("INSERT INTO users (username, badge_id, password_hash) VALUES (%s, %s, %s)", 
                       (username, badge_id, hashed_password))
        connection.commit()
        return {"message": "User registered successfully", "user_id": cursor.lastrowid}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        close_db_connection(connection)

# ✅ User Login (MySQL Direct)
@app.post("/login/")
def login_user(username: str, password: str):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s OR badge_id = %s", (username, username))
    db_user = cursor.fetchone()

    if not db_user or not verify_password(password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Protected Route (JWT Auth)
@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello, {user}. You have access to this protected route."}

# ✅ CRUD Operations

## 🟢 Add a criminal
@app.post("/criminals/")
def add_criminal(name: str, age: int, crime_type: str):
    result = create_criminal(name, age, crime_type)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

## 🔵 Get all criminals
@app.get("/criminals/")
def list_criminals():
    result = get_criminals()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

## 🟢 Add a case
@app.post("/cases/")
def add_case(case_title: str, description: str, date_reported: str, criminal_id: int):
    result = create_case(case_title, description, date_reported, criminal_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

## 🔵 Get all cases
@app.get("/cases/")
def list_cases():
    result = get_cases()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

## 🔎 Get cases by criminal ID
@app.get("/cases/{criminal_id}")
def get_cases_of_criminal(criminal_id: int):
    result = get_cases_by_criminal(criminal_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

## ❌ Delete a criminal
@app.delete("/criminals/{criminal_id}")
def remove_criminal(criminal_id: int):
    result = delete_criminal(criminal_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

## ❌ Delete a case
@app.delete("/cases/{case_id}")
def remove_case(case_id: int):
    result = delete_case(case_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
