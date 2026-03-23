from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.auth import verify_token  # fix typo from 'verfiy_token'

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extracts and verifies JWT, returns payload (user_id and role)
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    return payload


def admin_only(current_user: dict = Depends(get_current_user)):
    """
    Checks that the user is an admin.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def worker_only(current_user: dict = Depends(get_current_user)):
    """
    Checks that the user is a worker.
    """
    if current_user.get("role") != "worker":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Worker access required")
    return current_user