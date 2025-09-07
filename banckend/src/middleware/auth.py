from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from ..config.settings import settings

security = HTTPBearer()

def verify_token(token: str = Depends(security)):
    try:
        if settings.DISABLE_AUTH:
            return {"user_id": "test_user"}
        
        payload = jwt.decode(
            token.credentials, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )