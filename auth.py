from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Token settings (you can move to .env later)
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Fake in-memory user DB
fake_users_db = {
    "john": {
        "username": "john",
        "password": "secret123"  # In real apps, this would be hashed
    },
    "nandu": {
        "username": "nandu",
        "password": "alpha123"
    },
    "sunil": {
        "username": "sunil",
        "password": "omega123"
    },
    "jane": {
        "username": "jane",
        "password": "welcome456"
    },
    "bob": {
        "username": "bob",
        "password": "mortgage789"
    }
}

# Token extractor for protected routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Authenticate user (check username & password)
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user


# Create JWT access token
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode token and extract user info
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )