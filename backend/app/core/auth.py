from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status

SECRET_KEY ="supersecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30





def create_access_token(user_id: int, role: str):
    """
    Creates a JWT token containing user ID and role
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        # decode token properly into dict
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        return {"user_id": int(user_id), "role": role}  # convert user_id to int safely

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")