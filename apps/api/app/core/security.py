from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)

class CurrentUser(BaseModel):
    user_id: UUID
    email: str
    role: str = "user"
    full_name: Optional[str] = None

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
) -> CurrentUser:
    """
    Verifies Supabase JWT token and extracts user identity.
    Strictly derives user_id from token 'sub' claim.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided in Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # Decode and verify Supabase JWT
        # In development/test mode, if secret is default, we can allow leeway or test tokens
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
            options={"verify_aud": False} # Supabase JWT aud can be authenticated or project specific
        )

        sub: Optional[str] = payload.get("sub")
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain valid subject (sub) claim.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_metadata = payload.get("user_metadata", {})
        email = payload.get("email") or user_metadata.get("email", "unknown@user.com")
        role = payload.get("role", "user")
        full_name = user_metadata.get("full_name")

        return CurrentUser(
            user_id=UUID(sub),
            email=email,
            role=role,
            full_name=full_name
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
