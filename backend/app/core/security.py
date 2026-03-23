# app/core/security.py
from passlib.context import CryptContext

# Use Argon2 for hashing passwords (safe for long passwords)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plaintext password using Argon2.
    Returns the hashed password string.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a plaintext password against the hashed password.
    Returns True if they match, False otherwise.
    """
    if not password or not hashed:
        return False
    return pwd_context.verify(password, hashed)