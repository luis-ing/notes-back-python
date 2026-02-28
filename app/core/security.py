from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

if not hasattr(bcrypt, "__about__"):
    # create a minimal namespace with a ``__version__`` attribute.
    class _About:
        pass

    _About.__version__ = getattr(bcrypt, "__version__", "<unknown>")
    bcrypt.__about__ = _About


# configuration (fall back to defaults when env vars are missing)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# reusable instance that can be injected wherever we need to check a token
oauth2_scheme = HTTPBearer()


# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create JWT
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ---------------------------------------------------------------------------
# utility used as a "middleware"/dependency to validate incoming JWTs.
# this can be applied to route functions or routers (via `dependencies=`)
# and will raise a 401 if the token is missing, malformed, invalid or expired.

# Validate JWT token
def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # optional: verify payload contents, e.g. user_id exists
        if "user_id" not in payload:
            raise JWTError("missing user_id")
        return payload
    except JWTError as exc:
        # hide internal error message; token might be expired or invalid
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

