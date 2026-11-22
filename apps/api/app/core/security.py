from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
import httpx
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)

_jwks_client: Optional[PyJWKClient] = None

def get_jwks_client() -> Optional[PyJWKClient]:
    global _jwks_client
    if _jwks_client is None and settings.SUPABASE_URL and not settings.SUPABASE_URL.startswith("https://mock"):
        jwks_url = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"
        _jwks_client = PyJWKClient(jwks_url, cache_keys=True)
    return _jwks_client

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
    Supports HS256 (HMAC with secret), ES256/RS256 (Asymmetric JWKS),
    and direct Supabase GoTrue fallback verification.
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
        header = jwt.get_unverified_header(token)
        alg = header.get("alg", "HS256")
        payload = None

        if alg == "HS256":
            payload = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
        elif alg in ["ES256", "RS256"]:
            client = get_jwks_client()
            if client:
                try:
                    signing_key = client.get_signing_key_from_jwt(token)
                    payload = jwt.decode(
                        token,
                        signing_key.key,
                        algorithms=[alg],
                        options={"verify_aud": False}
                    )
                except Exception:
                    pass

        # Fallback to Supabase GoTrue Auth /auth/v1/user
        if not payload:
            if settings.SUPABASE_URL and not settings.SUPABASE_URL.startswith("https://mock"):
                auth_url = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1/user"
                key_to_use = settings.SUPABASE_ANON_KEY or settings.SUPABASE_SERVICE_ROLE_KEY
                headers = {
                    "apikey": key_to_use,
                    "Authorization": f"Bearer {token}"
                }
                with httpx.Client(timeout=10.0) as http_client:
                    res = http_client.get(auth_url, headers=headers)
                    if res.status_code == 200:
                        user_data = res.json()
                        sub = user_data.get("id")
                        user_meta = user_data.get("user_metadata", {})
                        return CurrentUser(
                            user_id=UUID(sub),
                            email=user_data.get("email") or "athlete@fitguide.ai",
                            role=user_data.get("role", "authenticated"),
                            full_name=user_meta.get("full_name")
                        )
            raise ValueError(f"Unable to verify authentication token signature with algorithm '{alg}'")

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
